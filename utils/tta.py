import os
import edge_tts

async def text_to_audio(text, output_file):
    """
    Converts text to an audio file using Edge-TTS.

    :param text: The text to convert to speech.
    :param output_file: The name of the output audio file.
    """
    communicate = edge_tts.Communicate(text, voice="en-US-JennyNeural")
    await communicate.save(output_file)

def read_text_file(file_path):
    """
    Reads the content of a text file.

    :param file_path: The path to the text file.
    :return: The content of the text file as a string.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def split_text(text, max_length=5000):
    """
    Splits text into chunks of a specified maximum length.

    :param text: The text to split.
    :param max_length: The maximum length of each chunk.
    :return: A list of text chunks.
    """
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

async def main(input_file, output_file):
    text = read_text_file(input_file)
    text_chunks = split_text(text)
    combined_audio = None

    for i, chunk in enumerate(text_chunks):
        temp_output = f'temp_part_{i}.mp3'
        await text_to_audio(chunk, temp_output)
        if combined_audio is None:
            combined_audio = temp_output
        else:
            combined_audio = combine_audio_files(combined_audio, temp_output)

    os.rename(combined_audio, output_file)
    print(f'Audio file saved as {output_file}')

def combine_audio_files(file1, file2):
    """
    Combines two audio files into one.

    :param file1: The first audio file.
    :param file2: The second audio file.
    :return: The name of the combined audio file.
    """
    from pydub import AudioSegment

    sound1 = AudioSegment.from_mp3(file1)
    sound2 = AudioSegment.from_mp3(file2)
    combined = sound1 + sound2

    combined_output = 'combined.mp3'
    combined.export(combined_output, format='mp3')

    os.remove(file1)
    os.remove(file2)

    return combined_output

if __name__ == "__main__":
    import sys
    import asyncio

    if len(sys.argv) != 3:
        print("Usage: python script.py input_text_file output_audio_file")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    asyncio.run(main(input_file, output_file))
