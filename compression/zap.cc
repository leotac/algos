// Author: leonardo.taccari@gmail.com (Leonardo Taccari)
/* 
A compressing algorithm for ASCII text files, as simple as
it gets.
The compressed file has a header with the characters sorted
by decreasing frequency and a body with a frequency-based
encoding.
A character encoding is simply a sequence of 0's 
followed by a sequence of 1's.
TODO:
    - simple statistic analysis
    - a couple of silly benchmarks
*/

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <map>
#include <cmath>
#include <algorithm>

using namespace std;

#define NUM_CHARS 256

int char_count[NUM_CHARS];

// Map the encoding (its index) to the character. Sorted vector.
// Then, the i-th "best" encoding correspond to the i-th most frequent characteri
vector<int> indices(NUM_CHARS); 

// String representation of the compressed encoding for each char (as int)
string encoding[NUM_CHARS]; 

// Used to sort by most frequent 
bool cmp(const int a, const int b) {
    return char_count[a] > char_count[b];
}

// Translate a character to a vector of bool (bitset)
void translateCharToBits(char cur_char, vector<bool> &v){
    v.clear();
    //cout << "Translate "<< cur_char << " to " << encoding[(int)cur_char]<<endl;
    const char* compressed_encoding = encoding[(int)cur_char].c_str();
    int i = 0;
    while(compressed_encoding[i] != '\0'){
        if(compressed_encoding[i] == '0') {
            //cout << "Found 0-";
            v.push_back(0);
        }
        if(compressed_encoding[i] == '1') {
            //cout << "Found 1-";
            v.push_back(1);
        }
        i++;   
    }
}

// Translate a vector of bool (bitset) to a character, given a vector containing
// the characters sorted by frequency (from most to least frequent)
char translateBitsToChar(vector<bool> &v, vector<char>& chars) {
    int ones = 0;
    for(bool val : v)
        if(val)
            ones++;
    int l = (int) v.size();
        
    // Compact, but slower than pre-computing the indices in a table
    int encoding_index = ((l-2)+1)*(l-2)/2 + ones;
    //cout << "Is: " <<chars[encoding_index-1] << endl;
    
    return chars[encoding_index-1];
    }

int main (int argc, char **argv) {
    
    string file_name = "";
    string output_name = "";
    bool extract = false;
    int c;
    while ((c = getopt (argc, argv, "f:o:xh")) != -1)
        switch (c)
            {
            case 'x':
                extract = true;
                break;            
            case 'f':
                file_name = string(optarg);
                break;
            case 'o':
                output_name = string(optarg);
                break;
            case 'h':
                cout << argv[0] << "\nCompress an ASCII text file creating a file with .zap extension.\nArguments:\n-f\t(required) input file\n-o\toutput file\n-x\tuncompress file\n";
                return 0;
            case '?':
                if (optopt == 'f' || optopt == 'o')
                    fprintf (stderr, "Option -%c requires an argument.\n", optopt);
                else if (isprint (optopt))
                    fprintf (stderr, "Unknown option `-%c'.\n-h for a list of options\n", optopt);
                else
                    fprintf (stderr,
                        "Unknown option character `\\x%x'.\n-h for a list of options\n",
                        optopt);
                return 1;
            default:
                return 1;
           }
    
    if (file_name == "") {
        cout << "-f required\n-h for a list of options\n";
        return 1;
    }

    ifstream ifile(file_name.c_str());
    if(!ifile) {
        cout << argv[0] << ": " << file_name << ": the file does not exist\n";
        return 1;
    }
    ifile.close();
 
    
    if (extract) {
        int lastindex = file_name.find_last_of("."); 
        if (lastindex == string::npos || file_name.substr(lastindex+1) != "zap") {
            cout << argv[0] << ": " << file_name << ": unknown suffix (expected .zap)\n";
            return 1;
        }
    }
    
    if (output_name == "") {
        if(!extract)
            output_name = file_name + ".zap";
        else {
            int lastindex = file_name.find_last_of("."); 
            output_name = file_name.substr(0, lastindex);
        }
    }
    
    
    /// Bitmasks used both for encoding and decoding
    char mask[8];
    mask[0]=0x80;
    mask[1]=0x40;
    mask[2]=0x20;
    mask[3]=0x10;
    mask[4]=0x08;
    mask[5]=0x04;
    mask[6]=0x02;
    mask[7]=0x01;

    // ENCODING
    if(!extract){
        // Initialize arrays/vectors
        for (int i=0;i<NUM_CHARS;++i) {
            char_count[i] = 0;
            indices[i] = i;
            //cout << (char) i << endl;
        }
        
        ifstream input1(file_name.c_str());
        stringstream buffer;
        buffer << input1.rdbuf();
        string contents(buffer.str());
        //cout << contents;
        for (char cur_char : contents) {
            if( (int)cur_char < 0 || (int)cur_char > NUM_CHARS) {
                cout << "Found a non-ASCII character. The input has to be strictly ASCII text.\n";
                return 1;
            }
                
            //cout << cur_char << " : " <<(int)cur_char;
            char_count[(int)cur_char]++;
            //cout<<"Count: "<<cur_char<<"  "<<char_count[(int)cur_char]<<endl;
        }
        
        sort(indices.begin(), indices.end(), cmp);
        
        for(int char_int : indices) {
            if(char_count[char_int]>0) {
                //cout << (char)char_int <<"  " << char_count[char_int]<< endl;
             }
        }
        
        /// Build the vector of translation char -> bitvector (as string)
        char ch;
        for(int index=0;index<NUM_CHARS;++index) {
            // As soon as we get a character with 0 occurences, break.
            if(char_count[indices[index]]==0)
                break;
            
            ch = (char) indices[index];
            //cout<<index<<":"<<ch<<"-";
            int floar = (int) floor((-1 + sqrt(1 + 8*index))/2);
            int length = floar + 2;
            int zeros = length -2 - (index - (floar+1)*(floar)/2);
            char* enc = new char[length+1];
            enc[0]='0';
            enc[length-1]='1';
            enc[length]='\0';
            for(int k=1;k<length-1;++k){
                if (k-1<zeros)
                    enc[k]='0';
                else
                    enc[k]='1';
            }
            //cout<<string(enc)<<"--"<<endl;
            //cout<<enc[length];
            encoding[(int)ch] = string(enc);
        }
            
        // Do the encoding
        char byte = 0x00;
        ofstream outbin(output_name.c_str(), ios::binary );
        int counter = 0;
        vector<bool> v;
        
        ifstream input(file_name.c_str());
        stringstream buffer1;
        buffer1 << input.rdbuf();
        string contents1(buffer1.str());
        
        // Write header: list of characters sorted by frequence
        for (int i = 0; i < (int)indices.size(); ++i) {
            char c = (char)indices[i];
            if (char_count[indices[i]] == 0)
                break;
            outbin.write(&c, sizeof(char));
        }
        outbin.write(".", sizeof(char));
        outbin.write(".", sizeof(char));
        
        // Write body of compressed file
        for (char cur_char : contents1) {
            //cerr<<"Read: "<<(int)cur_char<<endl;
            //cerr<<"Read: "<<cur_char<<endl;
                    
            vector<bool> v;
            translateCharToBits(cur_char, v); //get a character, spits out a vector of bits
        
            // Accumulate bits in byte
            // When byte is full, write it out
            for (unsigned int i=0; i<v.size(); ++i) {
                // If found a 1, write it. Else, just move right.
                if(v[i]==true)
                    byte = byte | mask[counter];
                counter++;
                // Byte full
                if (counter == 8){
                    //cout<<byte<<endl;
                    outbin.write( (&byte), sizeof( byte ) );
                    byte = 0x00;
                    counter = 0;
                }
            }
        }
        
        // If some bits are left over, write them out.
        if(counter>0)
            outbin.write( (&byte), sizeof( byte ) );
        outbin.close();
    }
    
    // DECODING
    if(extract) {
        char inbyte;
        ifstream inbin(file_name.c_str(), ios::binary);
        ofstream txtout(output_name.c_str());
        vector<bool> inbits;
        vector<char> outputz;
        vector<char> chars;
        bool last_was_one = false;
        bool gotChars = false;
        //cout<<endl;
        while(inbin.read(&inbyte, sizeof(inbyte))){
            if(!gotChars) {
                // Read header, with list of characters in the file 
                // sorted by frequency.
                // The header is delimited by two dots ".."
                if (inbyte == '.' && !chars.empty() && chars.back() == '.') {
                    gotChars = true;
                }
                chars.push_back(inbyte);
            } else {
                // Read the current char bit-by-bit using a sliding mask
                for(int i=0; i<8; ++i) {
                    if(((mask[i])&(inbyte)) == 0x00) {
                        // If this bit is 0 and the last was one, we have completed a character
                        // Translate the bits to char and write it out
                        if(last_was_one == true){
                            char ch = translateBitsToChar(inbits, chars);
                            //cout << ch << endl;
                            outputz.push_back(ch);
                            txtout << ch;
                            // Clear the vector
                            inbits.clear(); 
                            }
                        // Push a 0 in the current bitvector 
                        inbits.push_back(false);
                        last_was_one = false;
                    } else {
                        // Push a 1 in the current bitvector
                        inbits.push_back(true);
                        last_was_one = true;
                    }
                }
            }
        }
        
        txtout.close();
        
        //for (int i=0; i<(int)outputz.size(); ++i)
        //    cout << outputz[i];
        //cout<<endl<<"--"<<endl;
    
    }
}
