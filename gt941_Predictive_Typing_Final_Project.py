#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 16:45:43 2018

@author: georgetolkachev
"""

from sys import argv
import re
from contraction_list import contractions
from string import punctuation

def cleanup(word):
    word = word.lower();
    word = word.strip(punctuation);
    if word == "":
        return "INVALID";
    quotes = ["“", "”", "‘", "’"];
    for char in quotes:
        if char == word[0] or char == word[len(word) - 1]:
            word = word.strip(char);
        if word == "":
            return "INVALID";
    for char in word:
        if not char.isalpha() and char != "-" and char != "'":
            return "INVALID";
    return word;

filename = argv[1];

unigrams = {};
bigrams = {};
trigrams = {};
with open(filename) as f:
    line = f.readline();
    cntt = 0;
    while line:
        words = re.split(" |\t", line);
        words[len(words) - 1] = words[len(words) - 1].rstrip();
        u_count = 0;
        b_count = 0;
        t_count = 0;
        while u_count < len(words):
            unigram = cleanup(words[u_count]);
            if unigram == "INVALID":
                u_count += 1;
                b_count += 1;
                t_count += 1;
                continue;
            if unigram in contractions:
                expansion = re.split(" ", contractions[unigram]);
                for word in expansion:
                    if word not in unigrams.keys():
                        unigrams[word] = 1;
                    else:
                        unigrams[word] += 1;
            elif unigram[0].isalpha():
                if unigram not in unigrams.keys():
                    unigrams[unigram] = 1;
                else:
                    unigrams[unigram] += 1;
            if b_count < len(words) - 1:
                next_word = cleanup(words[b_count + 1]);
                if next_word == "INVALID":
                    u_count += 1;
                    b_count += 1;
                    t_count += 1;
                    continue;
                elif unigram[0].isalpha() and next_word[0].isalpha():
                    bigram = unigram + " " + next_word;
                    if bigram not in bigrams.keys():
                        bigrams[bigram] = 1;
                    else:
                        bigrams[bigram] += 1;
                if t_count < len(words) - 2:
                    next_next_word = cleanup(words[t_count + 2]);
                    if next_next_word == "INVALID":
                        u_count += 1;
                        b_count += 1;
                        t_count += 1;
                        continue;
                    elif unigram[0].isalpha() and next_word[0].isalpha() and next_next_word[0].isalpha():
                        trigram = unigram + " " + next_word + " " + next_next_word;
                        if trigram not in trigrams.keys():
                            trigrams[trigram] = 1;
                        else:
                            trigrams[trigram] += 1;
            u_count += 1;
            b_count += 1;
            t_count += 1;
        cntt += 1;
        line = f.readline();

alpha_unigrams = sorted(unigrams, key=lambda x: (x[0], -unigrams[x], x));
alpha_bigrams = sorted(bigrams, key=lambda x: (x[0], -bigrams[x], x));
alpha_trigrams = sorted(trigrams, key=lambda x: (x[0], -trigrams[x], x));
ordered_unigrams = {};
ordered_bigrams = {};
ordered_trigrams = {};
for key in alpha_unigrams:
    ordered_unigrams[key] = unigrams[key];
for key in alpha_bigrams:
    ordered_bigrams[key] = bigrams[key];
for key in alpha_trigrams:
    ordered_trigrams[key] = trigrams[key];
first_letter = [];
counters = [];
counter = 0;
for key in ordered_unigrams.keys():
    if key[0] not in first_letter:
        first_letter.append(key[0]);
        counters.append(counter);
    counter += 1;
first_letters = dict(zip(first_letter, counters));
first_letter2 = [];
counters2 = [];
counter = 0;
for key in ordered_bigrams.keys():
    if key[0] not in first_letter2:
        first_letter2.append(key[0]);
        counters2.append(counter);
    counter += 1;
first_letters2 = dict(zip(first_letter2, counters2));
first_letter3 = [];
counters3 = [];
counter = 0;
for key in ordered_trigrams.keys():
    if key[0] not in first_letter3:
        first_letter3.append(key[0]);
        counters3.append(counter);
    counter += 1;
first_letters3 = dict(zip(first_letter3, counters3));
ordered_unigram_list = [];
for item in ordered_unigrams.items():
    ordered_unigram_list.append(item);
ordered_bigram_list = [];
for item in ordered_bigrams.items():
    ordered_bigram_list.append(item);
ordered_trigram_list = [];
for item in ordered_trigrams.items():
    ordered_trigram_list.append(item);

overall_ksr_uni = 0;
overall_ksr_bi = 0;
overall_ksr_tri = 0;
cnnt = 0;
filename2 = argv[2];
with open(filename2) as f2:
    line = f2.readline();
    line_cnnt = 0;
    while line_cnnt < 30:
        words = re.split(" |\t", line);
        words[len(words) - 1] = words[len(words) - 1].rstrip();
        line_ksr_uni = 0;
        line_ksr_bi = 0;
        line_ksr_tri = 0;
        u_count = 0;
        b_count = 0;
        t_count = 0;
        while u_count < len(words):   
            curr_word = cleanup(words[u_count]);
            if curr_word == "INVALID":
                u_count += 1;
                b_count += 1;
                t_count += 1;
                continue;
            if curr_word in contractions:
                expansion = re.split(" ", contractions[curr_word]);
                curr_word = expansion[0];
                for i in range(len(expansion) - 1, 0, -1):
                    words.insert(u_count + 1, expansion[i]);
            curr_char_index = 1;
            word_so_far = "";
            options_list = [];
            ki = -1;
            uni_index = first_letters[curr_word[0]];
            next_index = counters[first_letter.index(curr_word[0]) + 1];
            while curr_char_index <= len(curr_word):
                curr_char = curr_word[curr_char_index - 1];
                word_so_far += curr_char;
                for i in range(uni_index, next_index):
                    if ordered_unigram_list[i][0][:curr_char_index] == word_so_far:
                        options_list.append(ordered_unigram_list[i][0]);
                    if len(options_list) == 3 or i == next_index - 1:
                        uni_index = i + 1;
                        break;
                ki += 1;
                curr_char_index += 1;
                if curr_word in options_list:
                    break;
                else:
                    options_list.clear();
            ks = 1;
            kn = len(curr_word);
            ksr = (1 - (ki + ks) / kn) * 100;
            overall_ksr_uni += ksr;
            line_ksr_uni += ksr;
            if line_cnnt == 0:
                print("-----------------");
                print("UNIGRAM MODEL:");
                print("The word is:", curr_word);
                print("The word so far is:", word_so_far);
                print("The keystroke savings rate for",  curr_word, "is:", ksr, "%");
            if b_count < len(words) - 1:
                next_word = cleanup(words[b_count + 1]);
                if next_word == "INVALID":
                    u_count += 1;
                    b_count += 1;
                    t_count += 1;
                    continue;
                else:
                    curr_words = curr_word + " " + next_word;
                    curr_char_index = 0;
                    words_so_far = curr_word + " ";
                    options_list = [];
                    ki = -1;
                    bi_index = first_letters2[curr_words[0]];
                    next_index = counters2[first_letter2.index(curr_words[0]) + 1];
                    while curr_char_index < len(next_word):
                        for i in range(bi_index, next_index):
                            if ordered_bigram_list[i][0][:len(curr_word) + 1 + curr_char_index] == words_so_far:
                                options_list.append(ordered_bigram_list[i][0]);
                            if len(options_list) == 60 or i == next_index - 1:
                                bi_index = i + 1;
                                break;
                        ki += 1;
                        if curr_words in options_list:
                            break;
                        else:
                            words_so_far += next_word[curr_char_index];
                            curr_char_index += 1;
                            if curr_char_index == len(next_word):
                                ki += 1;
                            options_list.clear();
                    ks = 0;
                    kn = len(next_word);
                    ksr = (1 - (ki + ks) / kn) * 100;
                    overall_ksr_bi += ksr;
                    line_ksr_bi += ksr;
                    if line_cnnt == 0:
                        print("-----------------");
                        print("BIGRAM MODEL:");
                        print("The words are:", curr_words);
                        print("The words so far are:", words_so_far);
                        print("The keystroke savings rate for",  curr_words, "is:", ksr, "%");
                    if t_count < len(words) - 2:
                        next_next_word = cleanup(words[t_count + 2]);
                        if next_next_word == "INVALID":
                            u_count += 1;
                            b_count += 1;
                            t_count += 1;
                            continue;
                        else:
                            curr_words = curr_word + " " + next_word + " " + next_next_word;
                            curr_char_index = 0;
                            curr_phrase = curr_word + " " + next_word;
                            words_so_far = curr_word + " " + next_word + " ";
                            options_list = [];
                            ki = -1;
                            tri_index = first_letters3[curr_words[0]];
                            next_index = counters3[first_letter3.index(curr_words[0]) + 1];
                            while curr_char_index < len(next_next_word):
                                for i in range(tri_index, next_index):
                                    if ordered_trigram_list[i][0][:len(curr_phrase) + 1 + curr_char_index] == words_so_far:
                                        options_list.append(ordered_trigram_list[i][0]);
                                    if len(options_list) == 120 or i == next_index - 1:
                                        tri_index = i + 1;
                                        break;
                                ki += 1;
                                if curr_words in options_list:
                                    break;
                                else:
                                    words_so_far += next_next_word[curr_char_index];
                                    curr_char_index += 1;
                                    if curr_char_index == len(next_next_word):
                                        ki += 1;
                                    options_list.clear();
                            ks = 0;
                            kn = len(next_next_word);
                            ksr = (1 - (ki + ks) / kn) * 100;
                            overall_ksr_tri += ksr;
                            line_ksr_tri += ksr;
                            if line_cnnt == 0:
                                print("-----------------");
                                print("TRIGRAM MODEL:");
                                print("The words are:", curr_words);
                                print("The words so far are:", words_so_far);
                                print("The keystroke savings rate for",  curr_words, "is:", ksr, "%");
            u_count += 1;
            b_count += 1;
            t_count += 1;
            cnnt += 1;
            if line_cnnt == 0 and u_count == len(words):
                print("-----------------");
                print("-----------------");
                print("-----------------");
                print("The average unigram ksr for this line is:", line_ksr_uni / (len(words)), "%");
                print("The average bigram for this line is:", line_ksr_bi / (len(words) - 1), "%");
                print("The average trigram for this line is:", line_ksr_tri / (len(words) - 2), "%");
                print("\n\n\n");
        if line_cnnt == 9:
            print("The average unigram ksr for block 1 is:", overall_ksr_uni / cnnt, "%");
            print("The average bigram ksr for block 1 is:", overall_ksr_bi / (cnnt - 10), "%");
            print("The average trigram ksr for block 1 is:", overall_ksr_tri / (cnnt - 20), "%");
            print("-----------------");
        if line_cnnt == 19:
            print("The average unigram ksr for block 2 is:", overall_ksr_uni / cnnt, "%");
            print("The average bigram ksr for block 2 is:", overall_ksr_bi / (cnnt - 10), "%");
            print("The average trigram ksr for block 2 is:", overall_ksr_tri / (cnnt - 20), "%");
            print("-----------------");
        if line_cnnt == 29:
            print("The average unigram ksr for block 3 is:", overall_ksr_uni / cnnt, "%");
            print("The average bigram ksr for block 3 is:", overall_ksr_bi / (cnnt - 10), "%");
            print("The average trigram ksr for block 3 is:", overall_ksr_tri / (cnnt - 20), "%");
            print("-----------------");
        if line_cnnt == 9 or line_cnnt == 19 or line_cnnt == 29:
            overall_ksr_uni = 0;
            overall_ksr_bi = 0;
            overall_ksr_tri = 0;
            cnnt = 0;
        line_cnnt += 1;
        line = f2.readline();