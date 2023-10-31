#include <stdio.h>
#include <stdbool.h>
#include <string.h>

void stream_pgn(const char *pgn_file, const char *outfile, int numGames)
{
    FILE *input = fopen(pgn_file, "r");
    FILE *output = fopen(outfile, "w");

    if (input == NULL || output == NULL)
    {
        perror("File opening failed");
        return;
    }

    int games = 0;
    char buffer[1024]; // Adjust the buffer size as needed
    bool game_started = false;

    while (fgets(buffer, sizeof(buffer), input) && games < numGames)
    {
        if (strncmp(buffer, "[Event ", 7) == 0)
        {
            if (game_started)
            {
                game_started = false; // Reset game_started if a new game starts
            }
            game_started = true;
        }

        if (game_started)
        {
            fputs(buffer, output);

            if (strcmp(buffer, "\n") == 0)
            {
                fseek(input, -1, SEEK_CUR); // Move the file pointer back by one character

                bool has_eval = false;
                while (fgets(buffer, sizeof(buffer), input) && strcmp(buffer, "\n") != 0)
                {
                    if (strstr(buffer, "%eval") != NULL)
                    {
                        has_eval = true;
                        break;
                    }
                }

                if (has_eval)
                {
                    games++;
                    printf("Processed %d games\r", games); // Progress indicator
                    fflush(stdout);                        // Flush the output to update the progress
                }
            }
        }
    }

    printf("\nProcessed %d games\n", games); // Print the final count
    fclose(input);
    fclose(output);
}

int main()
{
    const char *pgn_file = "./data/database.pgn";
    const char *outfile = "./data/evals.pgn";
    int numGames = 1000;

    stream_pgn(pgn_file, outfile, numGames);

    return 0;
}
