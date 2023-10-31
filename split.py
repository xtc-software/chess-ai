import os
import cProfile

# Set the path to your large PGN file and the folder to save the split files
pgn_file = './data/database.pgn'
output_folder = './data'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Function to split the PGN file
def split_pgn(pgn_file, num_files):
    with open(pgn_file, 'r', encoding='utf-8') as f:  # Specify the encoding here
        games = f.read().split('\n\n')

    # Calculate the number of games per file
    games_per_file = len(games) // num_files
    print(len(games))
    # Split the games into separate files
    for i in range(num_files):
        start_idx = i * games_per_file
        end_idx = (i + 1) * games_per_file if i < num_files - 1 else len(games)
        file_name = os.path.join(output_folder, f'split_{i+1}.pgn')

        with open(file_name, 'w', encoding='utf-8') as f_out:  # Specify the encoding for writing as well
            f_out.write('\n\n'.join(games[start_idx:end_idx]))

def stream_pgn(num_files, outfile, numGames):

    with open(pgn_file, 'r') as f, open(outfile, 'w') as out:
        games = 0
        buffer = ""
        for line in f:
            buffer += line
            if line == "\n":
                if "%eval" in buffer:
                    games += 1
                    out.write(buffer)
                
                buffer = ""
            
            #print(f"on game {games} out of {numGames} | {(games/numGames)*100}%", end="\r")
            if games >= numGames:
                break
            
# split_pgn(pgn_file, num_files=10)  # You can change the number of files as needed
cProfile.run('stream_pgn(num_files=10, outfile="./data/trimdatasmall.pgn", numGames=250000)')