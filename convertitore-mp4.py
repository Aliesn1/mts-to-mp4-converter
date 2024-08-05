import os
import subprocess
import sys

def check_ffmpeg_installed():
    try:
        subprocess.run(['ffmpeg', '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("ffmpeg è  installato.")
    except subprocess.CalledProcessError:
        print("ffmpeg non è installato.")
        sys.exit(1)

def convert_mts_to_mp4(input_file, output_file):
    command = [
        'ffmpeg',
        '-i', input_file,
        '-c:v', 'copy',  #Copia stream video senza re-encoding
        '-c:a', 'copy',  #Copia stream audio senza re-encoding
        output_file
    ]
    
    try:
        subprocess.run(command, check=True)
        print(f'File {input_file} convertito in {output_file}')
    except subprocess.CalledProcessError as e:
        print(f'Error :{e}')
    except FileNotFoundError:
        print("ffmpeg non trovato.")

def convert_all_mts_in_directory(directory):
    if not os.path.isdir(directory):
        print(f"la directory {directory} non esiste.")
        return
    
   #includo sia i file .mts che i file .MTS
   mts_files = [f for f in os.listdir(directory) if f.lower().endswith('.mts')]

    if not mts_files:
        print(f"Non ho trovato file .mts nella directory {directory}.")
        return

    for filename in mts_files:
        input_file = os.path.join(directory, filename)
        output_file = os.path.join(directory, f"{os.path.splitext(filename)[0]}.mp4")
        convert_mts_to_mp4(input_file, output_file)

# Example usage
if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Prendo i file dalla sub-directory 'video_mts'
    directory_path = os.path.join(script_directory, 'video_mts')
    
    # Controllo se è installato ffmpeg nel sistema
    check_ffmpeg_installed()
    
    # Converto tutti i file .mts della cartella 'video.mts' in mp4
    convert_all_mts_in_directory(directory_path)

