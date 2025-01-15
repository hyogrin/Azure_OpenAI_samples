import os
import pandas as pd
from jiwer import wer, cer
import glob

def evaluate_stt(
    wer_origin_path: str,
    wer_result_folder: str,
    output_csv: str = None
) -> pd.DataFrame:
    """
    1) Reads a text file `wer_origin_file` containing lines of 
       'wav_filename<TAB>original_transcript'.
    2) Loads each (wav_filename, original_transcript) into a DataFrame.
    3) For each wav_filename, finds the corresponding STT result text file 
       in `wer_result_folder` named `<wav_filename>.txt`.
    4) Computes WER and CER between the original transcript and the STT result.
    5) Returns a DataFrame with columns:
       ['wav_name', 'original_transcript', 'stt_transcript', 'WER', 'CER'].
    6) Optionally saves the DataFrame to `output_csv` if provided.
    """

    if os.path.isdir(wer_origin_path):
        temp_records = []
        for txt_file in glob.glob(os.path.join(wer_origin_path, "*.txt")):
            with open(txt_file, "r", encoding="utf-8") as f:
                for line in f:

                    wav_name = os.path.basename(txt_file).replace(".txt", "")
                    original_transcript = line.strip()
                    temp_records.append({"wav_name": wav_name, "original": original_transcript})
        df_original = pd.DataFrame(temp_records)
    else:
        df_original = pd.read_csv(
            wer_origin_path,
            sep="\t",
            names=["wav_name", "original"],
            header=None,
            encoding="utf-8"
        )

    results = []

    # Iterate over the rows in the original transcripts DataFrame
    for _, row in df_original.iterrows():
        wav_name = row["wav_name"]
        original_text = str(row["original"]).strip()

        # Construct the path to the STT result file
        stt_file_path = os.path.join(wer_result_folder, f"{wav_name}.txt")

        # If the file doesn't exist, skip it or handle error
        if not os.path.exists(stt_file_path):
            print(f"Warning: No STT result found for {wav_name}")
            continue

        # Read the STT transcription
        with open(stt_file_path, "r", encoding="utf-8") as f:
            stt_text = f.read().strip()

        # Compute WER and CER
        wer_score = wer(original_text, stt_text)
        cer_score = cer(original_text, stt_text)

        # Collect results
        results.append({
            "wav_name": wav_name,
            "original": original_text,
            "stt": stt_text,
            "WER": wer_score,
            "CER": cer_score
        })

    # Create a DataFrame of the results
    df_results = pd.DataFrame(results)

    # Optionally, save the results DataFrame to a CSV file
    if output_csv:
        df_results.to_csv(output_csv, index=False, encoding="utf-8")

    return df_results


import os
import pandas as pd
from jiwer import wer, cer
import difflib
import glob

correct = 'yellow'
deletion = 'red'
insertion = 'green'
substitution = 'purple'


def highlight_differences(original_text: str, stt_text: str):
    """
    Compare original_text and stt_text token by token
    using difflib.SequenceMatcher, and highlight:
      - Correct words in YELLOW
      - Deletions in RED
      - Insertions in GREEN
      - Substitutions in PURPLE
      
    """
    original_tokens = original_text.split()
    stt_tokens = stt_text.split()
    
    matcher = difflib.SequenceMatcher(None, original_tokens, stt_tokens)
    
    highlighted_original = []
    highlighted_stt = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            for token in original_tokens[i1:i2]:
                highlighted_original.append(
                    f"<span style='background-color: {correct}'>{token}</span>"
                )
            for token in stt_tokens[j1:j2]:
                highlighted_stt.append(
                    f"<span style='background-color: {correct}'>{token}</span>"
                )
        elif tag == 'delete':
            for token in original_tokens[i1:i2]:
                highlighted_original.append(
                    f"<span style='background-color: {deletion}'>{token}</span>"
                )
            # No tokens to highlight in STT for a pure deletion
        elif tag == 'insert':
            for token in stt_tokens[j1:j2]:
                highlighted_stt.append(
                    f"<span style='background-color: {insertion}'>{token}</span>"
                )
        elif tag == 'replace':
            for token in original_tokens[i1:i2]:
                highlighted_original.append(
                    f"<span style='background-color: {substitution}'>{token}</span>"
                )
            for token in stt_tokens[j1:j2]:
                highlighted_stt.append(
                    f"<span style='background-color: {substitution}'>{token}</span>"
                )
        
    # Join tokens back into strings
    highlighted_original_str = " ".join(highlighted_original)
    highlighted_stt_str = " ".join(highlighted_stt)
    
    return highlighted_original_str, highlighted_stt_str

def evaluate_stt_with_highlighting(
    wer_hl_origin_path: str,
    wer_result_folder: str,
    output_html: str = "stt_evaluation_results.html"
) -> pd.DataFrame:
    
    if os.path.isdir(wer_hl_origin_path):
        temp_records = []
        for txt_file in glob.glob(os.path.join(wer_hl_origin_path, "*.txt")):
            with open(txt_file, "r", encoding="utf-8") as f:
                for line in f:

                    wav_name = os.path.basename(txt_file).replace(".txt", "")
                    original_transcript = line.strip()
                    temp_records.append({"wav_name": wav_name, "original": original_transcript})
        df_original = pd.DataFrame(temp_records)
    else:
        df_original = pd.read_csv(
            wer_hl_origin_path,
            sep="\t",
            names=["wav_name", "original"],
            header=None,
            encoding="utf-8"
        )

    results = []

    # Iterate over the rows in the original transcripts DataFrame
    for _, row in df_original.iterrows():
        wav_name = row["wav_name"]
        original_text = str(row["original"]).strip()

        # Construct the path to the STT result file
        stt_file_path = os.path.join(wer_result_folder, f"{wav_name}.txt")

        # If the file doesn't exist, skip it or handle error
        if not os.path.exists(stt_file_path):
            print(f"Warning: No STT result found for {wav_name}")
            continue

        # Read the STT transcription
        with open(stt_file_path, "r", encoding="utf-8") as f:
            stt_text = f.read().strip()

        # Compute WER and CER (jiwer)
        wer_score = wer(original_text, stt_text)
        cer_score = cer(original_text, stt_text)

        # Highlight differences in HTML
        highlighted_original, highlighted_stt = highlight_differences(
            original_text, stt_text
        )

        # Collect results
        results.append({
            "wav_name": wav_name,
            "original": original_text,
            "stt": stt_text,
            "WER": wer_score,
            "CER": cer_score,
            "highlighted_original": highlighted_original,
            "highlighted_stt": highlighted_stt
        })

    # Create a DataFrame of the results
    df_results = pd.DataFrame(results)
    
    # Convert DataFrame to HTML with color-coded columns
    # Note: `escape=False` so we can display the HTML tags
    html_output = df_results.to_html(
        columns=["wav_name", "WER", "CER", 
                 "highlighted_original", "highlighted_stt"],
        index=False,
        escape=False
    )

    # Save the HTML to file
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_output)

    return df_results


