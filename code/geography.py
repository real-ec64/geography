#####################################################################
# Author      : Eric Chang                                          #
# Date        : 03/03/26                                            #
# Description : Quiz Time                                           #
# Last Edit   : EC 3/5/26                                           #
#####################################################################


##### SET UP ________________________________________________________

### Import Packages
import re
import random
import pandas as pd
from rapidfuzz import fuzz


### Import Data
data_orig = pd.read_csv('input/master.csv')
data_orig['gdp_pc'] = data_orig['gdp'] / data_orig['pop']

### Define Clean
def clean(s):
    return re.sub(r'[^a-z0-9]', '', str(s).lower())

##### INTRODUCTION __________________________________________________

start = 1
again = ''

while True:

    logs = pd.read_csv('input/logs.csv')
    logs = logs.fillna(0)
    logs_new = logs.copy()

    data = data_orig.copy()

    forfeit = False
    completed = False
    select = 0
    setup  = 0

    while setup == 0:

        if (start == 1):
            start = 2
            print()
            print('Welcome to the GEO quiz!')
            name = input('What is your name? ')
            print()
            player_log = logs[logs['player'] == name].copy()
            if (len(player_log) > 0):
                if (player_log['geo_master'].iloc[0] == 1):
                    print(f'Welcome back, Grand GEO master {name}, King of Capitals and ISOs!')
                elif (player_log['capitals_king'].iloc[0] == 1):
                    if (player_log['iso2_king'].iloc[0] == 1):
                        print(f'Welcome back {name}, king of Capitals and ISO2!')
                    elif (player_log['iso3_king'].iloc[0] == 1):
                        print(f'Welcome back {name}, king of Capitals and ISO3!')
                    else:
                        print(f'Welcome back {name}, king of Capitals')
                elif (player_log['iso2_king'].iloc[0] == 1):
                    if (player_log['iso3_king'].iloc[0] == 1):
                        print(f'Welcome back {name}, king of the ISOs!')
                    else:
                        print(f'Welcome back {name}, king of ISO2!')
                elif (player_log['iso3_king'].iloc[0] == 1):
                    print(f'Welcome back {name}, king of ISO3!')
                else:
                    print(f'Welcome back {name}!')
            else:
                print(f'Welcome to the GEO quiz, {name}!')
                logs_new.loc[len(logs_new)] = {'player': name}

        player_log = logs_new[logs_new['player'] == name].copy()

        if select == 0:
            print()
            print('Choose:')
            print('[1] Capitals')
            print('[2] ISO-2 Codes')
            print('[3] ISO-3 Codes')
            print('[4] Random')
            print('[5] Hall of Fame')
            print('[6] Change Players')
            print('[7] Help')
            print('[8] Quit')
            print()
            select = int(input('Main Choice: '))
            print()
        if (select > 0) & (select < 4):
            print('How many countries would you like? (Max 197)')
            while True:
                length = int(input('Country Choice: '))
                if length == 197:
                    print('A true challenger...')
                    setup = 1
                    break
                if (length < 197) & (length > 0):
                    print(f'Commencing with {length} countries')
                    setup = 1
                    break
                else:
                    print('Please enter valid input')

        elif select == 4:
            select = random.randint(1, 3)

        elif select == 5:
            print('**** HALL OF FAME ****')
            hall = logs.copy()
            hall['total'] = (hall['iso3_score'] * hall['iso3_num']) + (hall['iso2_score'] * hall['iso2_num']) + (hall['capitals_score'] * hall['capitals_num'])
            hall = hall.sort_values(by = 'total', ascending = False)
            if (hall['total'].iloc[0] > 0):
                print(f"**1** {hall['player'].iloc[0]}: {hall['total'].iloc[0]} points")
                print('     Awards:')
                if (hall['geo_master'].iloc[0] == 1):
                    print('     Grand GEO Master')
                if (hall['capitals_king'].iloc[0] == 1):
                    print('     Capitals King')
                if (hall['iso2_king'].iloc[0] == 1):
                    print('     ISO-2 King')
                if (hall['iso3_king'].iloc[0] == 1):
                    print('     ISO-3 King')
                if ((hall['capitals_king'].iloc[0] == 0) & (hall['iso2_king'].iloc[0] == 0) & (hall['iso3_king'].iloc[0] == 0)):
                        print('     Nothing to show here...')
                print(f"  Capital Stats: {hall['capitals_score'].iloc[0] * hall['capitals_num'].iloc[0]} points, {hall['capitals_score'].iloc[0]}% for {hall['capitals_num'].iloc[0]} countries")
                print(f"  ISO-2 Stats: {hall['iso2_score'].iloc[0] * hall['iso2_num'].iloc[0]} points, {hall['iso2_score'].iloc[0]}% for {hall['iso2_num'].iloc[0]} countries")
                print(f"  ISO-3 Stats: {hall['iso3_score'].iloc[0] * hall['iso3_num'].iloc[0]} points, {hall['iso3_score'].iloc[0]}% for {hall['iso3_num'].iloc[0]} countries")
                print()
                if (len(hall) > 1):
                    if (hall['total'].iloc[0] == hall['total'].iloc[1]):
                        print(f"**1** *{hall['player'].iloc[1]}*: ")
                    else:
                        print(f"*2* {hall['player'].iloc[1]}: ")
                    print('     Awards:')
                    if (hall['geo_master'].iloc[1] == 1):
                        print('     Grand GEO Master')
                    if (hall['capitals_king'].iloc[1] == 1):
                        print('     Capitals King')
                    if (hall['iso2_king'].iloc[1] == 1):
                        print('     ISO-2 King')
                    if (hall['iso3_king'].iloc[1] == 1):
                        print('     ISO-3 King')
                    if ((hall['capitals_king'].iloc[1] == 0) & (hall['iso2_king'].iloc[1] == 0) & (hall['iso3_king'].iloc[1] == 0)):
                        print('     Nothing to show here...')
                    print(f"  Capital Stats: {hall['capitals_score'].iloc[1]}% for {hall['capitals_num'].iloc[1]} countries")
                    print(f"  ISO-2 Stats: {hall['iso2_score'].iloc[1]}% for {hall['iso2_num'].iloc[1]} countries")
                    print(f"  ISO-3 Stats: {hall['iso3_score'].iloc[1]}% for {hall['iso3_num'].iloc[1]} countries")
                    print()
                    if (len(hall) > 2):
                        if (hall['total'].iloc[0] == hall['total'].iloc[1] == hall['total'].iloc[2]):
                            print(f"**1** *{hall['player'].iloc[2]}*: ")
                        elif (hall['total'].iloc[1] == hall['total'].iloc[2]):
                            print(f"*2* {hall['player'].iloc[2]}: ")
                        else:
                            print(f"3 {hall['player'].iloc[2]}: ")
                        print('     Awards:')
                        if (hall['geo_master'].iloc[2] == 1):
                            print('     Grand GEO Master')
                        if (hall['capitals_king'].iloc[2] == 1):
                            print('     Capitals King')
                        if (hall['iso2_king'].iloc[2] == 1):
                            print('     ISO-2 King')
                        if (hall['iso3_king'].iloc[2] == 1):
                            print('     ISO-3 King')
                        if ((hall['capitals_king'].iloc[2] == 0) & (hall['iso2_king'].iloc[2] == 0) & (hall['iso3_king'].iloc[2] == 0)):
                            print('     Nothing to show here...')
                        print(f"  Capital Stats: {hall['capitals_score'].iloc[2]}% for {hall['capitals_num'].iloc[2]} countries")
                        print(f"  ISO-2 Stats: {hall['iso2_score'].iloc[2]}% for {hall['iso2_num'].iloc[2]} countries")
                        print(f"  ISO-3 Stats: {hall['iso3_score'].iloc[2]}% for {hall['iso3_num'].iloc[2]} countries")
            else:
                print('Keep playing different quizzes to appear here. Nothing to see here yet...')

            print('[1] Go Back')
            print('[2] Quit')

            while True:
                second_choice = int(input('Choice: '))
                if second_choice == 1:
                    select = 0
                    break
                if second_choice == 2:
                    select = 8
                    again = 'n'
                    break
                else:
                    print('Please enter a valid input.')

        elif select == 6:
            start = 1
            select = 0

        elif select == 7:
            print('Welcome to the world geo quiz! Will you complete to be the GEO Master?')
            print('First, choose what you would like to be tested on: capitals of the world,')
            print('or ISO Codes (2-3 character abbreviations based on the International Organization')
            print('for Standardization, ISO 3166 codes).')
            print('Second, choose how many countries you would like to be tested on (Max 197).')
            print("Type 'idk' to give up the question, and 'Quit' to forfeit the game.")
            print('Good luck!')
            print('[1] Go Back')
            print('[2] Quit')

            while True:
                second_choice = int(input('Choice: '))
                if second_choice == 1:
                    select = 0
                    break
                if second_choice == 2:
                    select = 8
                    again = 'n'
                    break
                else:
                    print('Please enter a valid input.')

        elif select == 8:
            again = 'n'
            break
        else:
            print('Please enter valid input')
            select = 0


    ##### CAPITALS __________________________________________________

    if select == 1:
        print()
        print('---Capitals---')

        if (len(player_log) > 0):
            if (player_log['capitals_score'].iloc[0] > 0):
                old_score = player_log['capitals_score'].iloc[0]
                old_num = player_log['capitals_num'].iloc[0]
                print(f'(Old high score: {old_score} with {old_num} countries)')

        total = 197

        data = data.sample(n=length).reset_index(drop=True)

        for country in data['country_name']:
            if forfeit == True:
                break
            print()
            print(f'-{country}-')

            answer = data.loc[data['country_name'] == country, 'capital'].iloc[0]
            answer_clean = clean(answer)

            attempt = 1
            while attempt < 4:
                resp = clean(input('Capital: '))
                if(resp == 'quit'):
                    forfeit = True
                    break
                elif(resp != answer_clean):
                    if (len(answer_clean) <= 4):
                        if((fuzz.ratio(resp, answer_clean) < 100) & (fuzz.ratio(resp, answer_clean) > 74)):
                            print('typo?')
                        else: continue
                    elif (fuzz.ratio(resp, answer_clean) < 100) & (fuzz.ratio(resp, answer_clean) > 82):
                        print('typo?')
                    else:
                        print('fail')
                        attempt = attempt + 1
                        if (attempt ==4) | (resp == 'idk'):
                            attempt = 4
                            print(f'Capital is: {answer}')
                else:
                    print('pass')
                    if attempt == 1:
                        data.loc[data['country_name'] == country, 'point'] = 1
                    if attempt == 2:
                        data.loc[data['country_name'] == country, 'point'] = .5
                    if attempt == 3:
                        data.loc[data['country_name'] == country, 'point'] = .25
                    attempt = 4
        
        if forfeit == False:
            completed = True
        elif forfeit == True:
            completed = False


    ##### ISO-2 _____________________________________________________

    if select == 2:
        print()
        print('---ISO-2---')

        if (len(player_log) > 0):
            if (player_log['iso2_score'].iloc[0] > 0):
                old_score = player_log['iso2_score'].iloc[0]
                old_num = player_log['iso2_num'].iloc[0]
                print(f'(Old high score: {old_score} with {old_num} countries)')

        total = 197

        data = data.sample(n=length).reset_index(drop=True)

        for country in data['country_name']:
            if forfeit == True:
                break
            print()
            print(f'-{country}-')

            answer = data.loc[data['country_name'] == country, 'iso2'].iloc[0]
            answer_clean = clean(answer)

            attempt = 1
            while attempt < 4:
                resp = clean(input('ISO-2: '))

                if(resp == 'quit'):
                    forfeit = True
                    break
                elif(resp != answer_clean):
                    print('fail')
                    attempt = attempt + 1
                    if (attempt ==4) | (resp == 'idk'):
                        attempt = 4
                        print(f'ISO-2 is: {answer}')
                else:
                    print('pass')
                    if attempt == 1:
                        data.loc[data['country_name'] == country, 'point'] = 1
                    if attempt == 2:
                        data.loc[data['country_name'] == country, 'point'] = .8
                    if attempt == 3:
                        data.loc[data['country_name'] == country, 'point'] = .6
                    attempt = 4
        
        if forfeit == False:
            completed = True
        elif forfeit == True:
            completed = False

    ##### ISO-3 _____________________________________________________

    if select == 3:
        print()
        print('---ISO-3---')

        if (len(player_log) > 0):
            if (player_log['iso3_score'].iloc[0] > 0):
                old_score = player_log['iso3_score'].iloc[0]
                old_num = player_log['iso3_num'].iloc[0]
                print(f'(Old high score: {old_score} with {old_num} countries)')

        data = data.sample(n=length).reset_index(drop=True)

        for country in data['country_name']:

            if forfeit == True:
                break

            print()
            print(f'-{country}-')

            answer = data.loc[data['country_name'] == country, 'iso3'].iloc[0]
            answer_clean = clean(answer)

            attempt = 1
            while attempt < 4:
                resp = clean(input('ISO-3: '))

                if(resp == 'quit'):
                    forfeit = True
                    break
                if(resp != answer_clean):
                    print('fail')
                    attempt = attempt + 1
                    if (attempt ==4) | (resp == 'idk'):
                        attempt = 4
                        print(f'ISO-3 is: {answer}')
                else:
                    print('pass')
                    if attempt == 1:
                        data.loc[data['country_name'] == country, 'point'] = 1
                    if attempt == 2:
                        data.loc[data['country_name'] == country, 'point'] = .75
                    if attempt == 3:
                        data.loc[data['country_name'] == country, 'point'] = .5
                    attempt = 4
        
        if forfeit == False:
            completed = True
        elif forfeit == True:
            completed = False


    ##### CONCLUSION ________________________________________________

    if completed == True:
        total = data['point'].sum()
        perc  = int(total/length) * 100
        print()
        print(f'---Final Report: {total}/{length} ({perc}%)---')

        if perc == 100:
            if length == 197:
                if select == 1:
                    if player_log['capitals_king'].iloc[0] == 1:
                        print("You've done it again, Capital King! Do you dare try our other quizzes?")
                    else:
                        logs_new.loc[logs_new['player'] == name, 'capitals_king'] = 1
                        print('You are the true CAPITAL Master! Do you dare try our other quizzes?')
                if select == 2:
                    if player_log['iso2_king'].iloc[0] == 1:
                        print("You've done it again, ISO-2 King! Do you dare try our other quizzes?")
                    else:
                        logs_new.loc[logs_new['player'] == name, 'iso2_king'] = 1
                        print('You are the true ISO-2 Master! Do you dare try our other quizzes?')
                if select == 3:
                    if player_log['iso3_king'].iloc[0] == 1:
                        print("You've done it again, ISO-3 King! Do you dare try our other quizzes?")
                    else:
                        logs_new.loc[logs_new['player'] == name, 'iso3_king'] = 1
                        print('You are the true ISO-3 Master! Do you dare try our other quizzes?')
                if (player_log['iso2_king'].iloc[0] == 1) & (player_log['iso3_king'].iloc[0] == 1) & (player_log['capitals_king'].iloc[0] == 1):
                    print('You have completed the GEO challenge and are officially the GEO master! Congratulations')
            else:
                print('perfect')
        if ((perc < 100) & (perc >= 93)):
            print('close')
        if ((perc < 93) & (perc >= 77)):
            print('above average')
        if ((perc < 77) & (perc >= 50)):
            print('average')
        if ((perc < 50) & (perc >= 37)):
            print('below average')
        if ((perc < 37) & (perc >= 20)):
            print('bad')
        if (perc < 20):
            print('horrible job!')


        if select == 1:
            if (total * 100 >= player_log['capitals_score'].iloc[0] * player_log['capitals_num'].iloc[0]) | (player_log['capitals_score'].iloc[0] == 0):
                    logs_new.loc[logs_new['player'] == name, 'capitals_score'] = perc
                    logs_new.loc[logs_new['player'] == name, 'capitals_num'] = length
                    print(f'New High Score! {perc}% with {length} countries')
        if select == 2:
            if (total * 100 >= player_log['iso2_score'].iloc[0] * player_log['iso2_num'].iloc[0]) | (player_log['iso2_score'].iloc[0] == 0):
                    logs_new.loc[logs_new['player'] == name, 'iso2_score'] = perc
                    logs_new.loc[logs_new['player'] == name, 'iso2_num'] = length
                    print(f'New High Score! {perc}% with {length} countries')
        if select == 3:
            if (total * 100 >= player_log['iso3_score'].iloc[0] * player_log['iso3_num'].iloc[0]) | (player_log['iso3_score'].iloc[0] == 0):
                    logs_new.loc[logs_new['player'] == name, 'iso3_score'] = perc
                    logs_new.loc[logs_new['player'] == name, 'iso3_num'] = length
                    print(f'New High Score! {total}: {perc}% with {length} countries')

        logs_new = logs_new.dropna(subset = ['capitals_score', 'iso3_score', 'iso2_score'], how = 'all')
        logs_new.to_csv('input/logs.csv', index = False)

    while (again != 'n'):
        again = clean(input('Play again? [Y/N]   ' ))
        if (again == 'n') | (again == 'y'):
            break
        print('What?')
        
    if again == 'n':
        print('Have a Geo-ful day!')
        break
    if again == 'y':
        print('Challenge accepted.')
