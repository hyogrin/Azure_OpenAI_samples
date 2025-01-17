import os
import glob
import difflib
import pandas as pd
from jiwer import wer, cer
from enum import Enum

# Colors for highlighting
correct = 'yellow'
deletion = 'red'
insertion = 'green'
substitution = 'purple'

class OriginFileType(Enum):
    SINGLE_LINE_TRAINING = 1
    MULTI_LINE = 2

def highlight_differences(original_text: str, stt_text: str):
    """
    Compare original_text and stt_text token by token using difflib.SequenceMatcher,
    applying color-coded highlights for equal, delete, insert, replace.
    """
    original_tokens = original_text.split()
    stt_tokens = stt_text.split()
    matcher = difflib.SequenceMatcher(None, original_tokens, stt_tokens)

    hi_orig, hi_stt = [], []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            hi_orig += [f"<span style='background-color:{correct}'>{t}</span>"
                        for t in original_tokens[i1:i2]]
            hi_stt += [f"<span style='background-color:{correct}'>{t}</span>"
                       for t in stt_tokens[j1:j2]]
        elif tag == 'delete':
            hi_orig += [f"<span style='background-color:{deletion}'>{t}</span>"
                        for t in original_tokens[i1:i2]]
        elif tag == 'insert':
            hi_stt += [f"<span style='background-color:{insertion}'>{t}</span>"
                       for t in stt_tokens[j1:j2]]
        elif tag == 'replace':
            hi_orig += [f"<span style='background-color:{substitution}'>{t}</span>"
                        for t in original_tokens[i1:i2]]
            hi_stt += [f"<span style='background-color:{substitution}'>{t}</span>"
                       for t in stt_tokens[j1:j2]]

    return " ".join(hi_orig), " ".join(hi_stt)

def evaluate_stt(
    origin_file_type: OriginFileType,
    origin_path: str,
    stt_folder: str,
    output_csv: str = None,
    output_html: str = None
) -> pd.DataFrame:
    """
    Evaluate WER/CER between original transcripts and STT results, 
    avoiding duplicate results by ensuring we only match each origin file 
    to its corresponding STT file once.
    """
    results = []

    # ---------------------------
    # SINGLE-LINE MODE
    # ---------------------------
    if origin_file_type == OriginFileType.SINGLE_LINE_TRAINING:
        if os.path.isdir(origin_path):
            raise ValueError("SINGLE_LINE_TRAING mode requires a file, not a directory.")

        df_original = pd.read_csv(
            origin_path,
            sep="\t",
            names=["wav_name", "original"],
            header=None,
            encoding="utf-8"
        )

        for _, row in df_original.iterrows():
            wav_name = row["wav_name"]
            original_text = str(row["original"]).strip()
            stt_file = os.path.join(stt_folder, f"{wav_name}.txt")
            if not os.path.exists(stt_file):
                print(f"Warning: no STT found for '{wav_name}'")
                continue

            with open(stt_file, "r", encoding="utf-8") as f:
                stt_text = f.read().strip()

            # Compute metrics and highlight
            wer_score = wer(original_text, stt_text)
            cer_score = cer(original_text, stt_text)
            hi_orig, hi_stt = highlight_differences(original_text, stt_text)

            results.append({
                "wav_name": wav_name,
                "original_transcript": original_text,
                "stt_transcript": stt_text,
                "WER": wer_score,
                "CER": cer_score,
                "highlighted_original": hi_orig,
                "highlighted_stt": hi_stt
            })

    # ---------------------------
    # MULTI-LINE MODE
    # ---------------------------
    elif origin_file_type == OriginFileType.MULTI_LINE:
        if not os.path.isdir(origin_path):
            raise ValueError("MULTI_LINE mode requires a directory.")

        origin_files = glob.glob(os.path.join(origin_path, "*.txt"))
        if not origin_files:
            print(f"No .txt files found in '{origin_path}'.")
            return pd.DataFrame()

        for origin_txt_file in origin_files:
            wav_name = os.path.splitext(os.path.basename(origin_txt_file))[0]
            stt_file = os.path.join(stt_folder, f"{wav_name}.txt")

            if not os.path.exists(stt_file):
                print(f"Warning: No STT file found for '{wav_name}'")
                continue

            # Read all lines
            with open(origin_txt_file, "r", encoding="utf-8") as f:
                origin_lines = [line.strip() for line in f]
            with open(stt_file, "r", encoding="utf-8") as f:
                stt_lines = [line.strip() for line in f]

            # Compare line by line
            max_len = min(len(origin_lines), len(stt_lines))
            if len(origin_lines) != len(stt_lines):
                print(
                    f"Warning: line count mismatch for '{wav_name}'. "
                    f"Comparing first {max_len} lines."
                )

            for i in range(max_len):
                orig_line = origin_lines[i]
                stt_line = stt_lines[i]
                wer_score = wer(orig_line, stt_line)
                cer_score = cer(orig_line, stt_line)
                hi_orig, hi_stt = highlight_differences(orig_line, stt_line)

                results.append({
                    "wav_name": wav_name,
                    "original_transcript": orig_line,
                    "stt_transcript": stt_line,
                    "WER": wer_score,
                    "CER": cer_score,
                    "highlighted_original": hi_orig,
                    "highlighted_stt": hi_stt
                })

    # Build the final DataFrame once
    df_results = pd.DataFrame(results)

    # Remove duplicates by wav_name + original_transcript + stt_transcript
    df_results.drop_duplicates(
        subset=["wav_name", "original_transcript", "stt_transcript"],
        keep="first",
        inplace=True
    )

    # Optional outputs
    if output_html:
        html = df_results.to_html(
            columns=["wav_name", "WER", "CER", "highlighted_original", "highlighted_stt"],
            index=False,
            escape=False
        )
        with open(output_html, "w", encoding="utf-8") as f:
            f.write(html)

    if output_csv:
        df_results.to_csv(output_csv, index=False, encoding="utf-8")

    return df_results