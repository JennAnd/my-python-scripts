# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 1
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:
    
import pandas as pd
import matplotlib.pyplot as plt

# Skapar tre DataFrame-objekt som motsvarar innehållet i de tre csv-filerna
df_cpi = pd.read_csv('cpi.csv', sep = ';', encoding = 'latin_1')
df_regions = pd.read_csv('regions.csv', sep = ';', encoding = 'latin_1')
df_inflation = pd.read_csv('inflation.csv', encoding ='utf-8', index_col='LOCATION')

# Kopplar ihop cpi.csv och regions.csv
df_cpi_merged = pd.merge(df_regions[['Land','Landskod','Kontinent']], df_cpi, on='Landskod')

# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 2
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:
# 2a

valda_lander = []  # Tom lista där användarens valda länder samlas
# Loopar input-texten max 3 gånger
while len(valda_lander) < 3:
    valda_lander_input = input("Ange namnet på landet som du vill analysera: ")
    if valda_lander_input.upper() == 'END':
        break
    
    try:  # Hanterar ifall användaren matar in fel i inputen
        if valda_lander_input in df_cpi_merged['Land'].values:
            valda_lander.append(valda_lander_input) # Hämtar de valda länderna från inputen och samlar i valda_lander för plottning längre ner
        else:
            raise ValueError("Felaktig inmatning. Försök igen.")
    except ValueError as ve:
        print(ve)  # ValueError printas med vald text ifall inmatning är fel av användaren

filt_valda_lander = df_cpi_merged[df_cpi_merged['Land'].isin(valda_lander)]
filt_valda_lander = filt_valda_lander.drop(columns=['Kontinent', 'Landskod']) # Filtrerar bort kolumner som ej ska användas i plottningen

filt_valda_lander = filt_valda_lander.set_index('Land')
plt.figure(figsize=(12,6))

# Linjediagram
for index, row in filt_valda_lander.iterrows():
    plt.plot(row.index, row.values, label=f'{index}') # Plottning av förändringen per rad av det land som väljs av användaren
    
    max_index = row.idxmax()  # Hittar de högsta värdet för att senare markera det i diagrammet med en liten cirkel
    min_index = row.idxmin()  # Hittar de lägsta värdet för att senare markera det i diagrammet med en liten cirkel

    plt.scatter(max_index, row[max_index], color='red', marker='o')  # Använder scatter för att plotta en liten cirkel på högsta och
    plt.scatter(min_index, row[min_index], color='blue', marker='o') # lägsta värderna i diagrammet

    
# Sätter titel på diagram, x- och y-axeln
plt.title("Årlig inflationstakt under åren 1960-2022")
plt.xlabel("År")
plt.ylabel("Inflationstakt [%]")

# Roterar årtalen på x-axeln
plt.xticks(rotation=90, ha="right")

# Sätter grid, visar etiketterna som sattes i label och visar diagrammet
plt.grid(True)
plt.legend()
plt.show()
 

# 2b

valt_land = []  # Tom lista där användarens valda land samlas
# Loopar input-texten max 3 gånger
while len(valt_land) < 1:
    valt_land_input = input("Ange namnet på landet som du vill analysera: ")
    
    try:  # Hanterar ifall användaren matar in fel i inputen
        if valt_land_input in df_cpi_merged['Land'].values:
            valt_land.append(valt_land_input) # Hämtar det valda landet från inputen och samlar i valt_land för plottning längre ner
        else:
            raise ValueError("Felaktig inmatning. Försök igen.")
    except ValueError as ve:
        print(ve)  # ValueError printas med vald text ifall inmatning är fel av användaren

filt_valt_land = df_cpi_merged[df_cpi_merged['Land'].isin(valt_land)]
filt_valt_land = filt_valt_land.drop(columns=['Kontinent', 'Landskod']) # Filtrerar bort kolumner som ej ska användas i plottningen

filt_valt_land = filt_valt_land.set_index('Land')
plt.figure(figsize=(12,6))

# Plottar förändringsfaktorn från valt land i stapeldiagram
for index, row in filt_valt_land.iterrows():  # Använder itterows() för att iterera över raderna
    forandrings_faktor = row.pct_change() * 100  # Beräknar förändringsfaktorn
    plt.bar(forandrings_faktor.index, forandrings_faktor.values, label=f'{index}')
        
# Sätter titel på diagram, x- och y-axeln
plt.title("Årlig inflationstakt under åren 1960-2022")
plt.xlabel("År")
plt.ylabel("Inflationstakt [%]")

# Roterar årtalen på x-axeln
plt.xticks(rotation=90, ha="right")

# Sätter grid, visar etiketterna som sattes i label och visar diagrammet
plt.grid(True)
plt.legend()
plt.show() 
   

# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 3
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

while True:  # Loop som fortsätter tills användaren fyllt i giltigt årtal
    valt_artal = input("Ange vilket år som ska analyseras: ")
    
    if not valt_artal.isdigit():  # Användaren måste fylla i endast siffror i inputen
        print("Felaktig inmatning. Årtalet måste anges som siffror.")
        continue  # Loopen börjar om ifall man ej skrivit siffror i inputen
    
    artal = int(valt_artal)
    
    if not (1960 <= artal <= 2022):  # Valt årtal måste vara mellan 1960-2022
        print("Angivet årtal finns inte. Var god väl ett nytt årtal mellan 1960-2022.")
        continue  # Loopen börjar om ifall årtalet inte finns
        
    break  # Loopen avslutas när användaren fyllt i giltigt årtal och resten av koden fortsätter

# Välj ut de 6 högsta och 6 lägsta värderna av valt årtal
lagsta_hogsta_varden = pd.concat([df_cpi_merged[valt_artal].nsmallest(6), df_cpi_merged[valt_artal].nlargest(6).sort_values(ascending=True)])

varden_lander = df_cpi_merged.loc[lagsta_hogsta_varden.index, 'Land'] # Hämtar ut motsvarande länder till värderna då de ska med i tabellen

# Skapa en ny DataFrame med informationen från värderna och motsvarande länder
varden_lander_df = pd.DataFrame({'Förändring [%]': lagsta_hogsta_varden.values, 'Land': varden_lander.values})

# TABELLEN
print(f"{'-'*100}")
print(f"{'-'*100}")
print(f"{'LÄNDER MED HÖGST OCH LÄGST INFLATION ÅR: '+valt_artal:^100}")
print(f"{'-'*100}")
print(f"{'Lägst':<56}{'Högst':<60}")
print("-----                                                   -----")
print(f'{"Land":<28}{"inflation [%]":<28}{"Land":<28}{"inflation [%]":<28}')
print(f"{'-'*100}")

# Loop för att skriva ut de lägsta och högsta värdena under varandra
for i in range(6):  # Separerar värderna och länderna beroende på högsta eller lägsta värden för tabellstrukturen
    lander_lagsta = varden_lander_df['Land'].iloc[i][:20]  # Sätter max 20 tecken på landsnamnet pga kan ta för mycket plats annars
    lander_hogsta = varden_lander_df['Land'].iloc[i + 6][:20]
    varden_lagsta = varden_lander_df['Förändring [%]'].iloc[i]
    varden_hogsta = varden_lander_df['Förändring [%]'].iloc[i + 6]
        
    print(f"{lander_lagsta:<27} {varden_lagsta:<27.2f} {lander_hogsta:<27} {varden_hogsta:<20.2f}")  # Denna rad är med i for-loopen för att alla 12 länder ska komma med i tabellen
print(f"{'-'*100}")
print(f"{'-'*100}")

# DIAGRAMMET
fig = plt.figure(figsize=(12, 6))

# Ange storleken och positionen för axeln inom figuren
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

# Skapa stapeldiagrammet på den givna axeln
ax.bar(varden_lander_df['Land'], varden_lander_df['Förändring [%]'])

# Anger labels och titel
ax.set_title(f'De lägsta och högsta inflationerna uppmätta år:{valt_artal}')
ax.set_xlabel(".")
ax.set_ylabel("Förändring [%]")

# Anger positionerna och etiketterna för x-axeln
ax.set_xticks(range(len(varden_lander_df['Land'])))
ax.set_xticklabels(varden_lander_df['Land'], rotation=45, ha="right")

# Sätta y-axelns lägsta värde
ax.set_ylim(bottom=lagsta_hogsta_varden.min() * 1)

plt.grid(True)
plt.show()

# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 4
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:
    
print(f"{'-'*100}")
print(f"{'-'*100}")
print(f"{'OLIKA KONTINENTERS INFLATION UNDER':^100}")
print(f"{'TIDSPERIODEN 1960 -- 2022':^100}")
print(f"{'-'*100}")
print(f"{'Högst':>33}{'Lägst':>28}{'Medel 1960-2022':>33}")
print(f'{"Kontinent/Land":<28}')
print(f'{"Inf [%] År":>38}{"Inf [%] År":>28}{"Inf [%]":>20}')
print(f"{'-'*100}")

kontinenter = df_cpi_merged['Kontinent'].unique()   # Hämta unika kontinenter då de står flera gånger i filen

# Tabellen med alla värden

i = 0

while i < len(kontinenter):   # Skriver ut alla kontinenter från listan kontinenter för att kunna skriva ut kontinent och medelvärde
    
    try:
        kontinent = kontinenter[i]
        medelvarde = df_cpi_merged[df_cpi_merged['Kontinent'] == kontinent].loc[:, '1960':'2022'].mean(axis=1).mean().round(1)  # Beräknar medelvärdet per kontinent, avrundat till en decimal
        print(f'{kontinent}{medelvarde:>79}')   # Här läggs kontinent och tillhörande medelvärde i tabellen
        i += 1
    except Exception as e:  # Hanterar eventuella fel
        print(f"Ett fel uppstod: {e}")
        break
   
    
# Loppar högsta värden med motsvarande årtal och land i tabellen
    hogsta_varden = df_cpi_merged.loc[df_cpi_merged['Kontinent'] == kontinent, '1960':'2022'].stack().sort_values(ascending=False).head(3)  # Med ascending=False hämtas de 3 högsta värderna
    for index, value in hogsta_varden.items():
        artal = f"{index[1]}"
        inf = f"{value:.1f}"
        land = f"{df_cpi_merged.loc[index[0], 'Land'][:20]}"
        print(f' {land:<23}{inf:^14}{artal}')
    
# Loppar lägsta värden med motsvarande årtal och land i tabellen
    lagsta_varden = df_cpi_merged.loc[df_cpi_merged['Kontinent'] == kontinent, '1960':'2022'].stack().sort_values(ascending=True).head(3)  # Med ascending=True hämtas de 3 lägsta värderna
    for index, value in lagsta_varden.items():
        artal = f"{index[1]}"
        inf = f"{value:.1f}"
        land = f"{df_cpi_merged.loc[index[0], 'Land'][:20]}"
        print(f' {land:<55}{inf:<9}{artal}')
        
    print() #Lägger till mellanrum mellan varje loop
    
# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 5
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

# Mergar ihop df_inflation och df_regions för att få med länderna
df_inflation = pd.merge(df_inflation, df_regions[['Landskod', 'Land']], left_on='LOCATION', right_on='Landskod', how='left')


# Byter namn på kolumnen med länder i till COUNTRY
df_inflation.rename(columns={'Land': 'COUNTRY'}, inplace=True)
df_inflation = df_inflation.drop('Landskod', axis=1)  # Landskod lades även till så tog bort den från df_inflation då den inte behövs

# Skapa en tom lista för att lagra valda kolumner
input_values = []  # Tom lista där användarens valda värden samlas


# Loopar alla fyra input-texterna max 1 gång om man väljer ett värde som finns
while len(input_values) < 1:
    country = input("Ange vilket land som ska analyseras: ")
    subject = input("Ange vilken subject du vill analysera: ")
    frequency = input("Ange vilken frequency du vill analysera: ")
    measure = input("Ange vilken measure du vill analysera: ")
    
    
    if country in df_inflation['COUNTRY'].values:
            input_values.append(country) # Hämtar valt country från inputen och samlar i values för plottning
    
    if subject in df_inflation['SUBJECT'].values:
            input_values.append(subject) # Hämtar valt subject från inputen och samlar i values för plottning
            
    if frequency in df_inflation['FREQUENCY'].values:
            input_values.append(frequency) # Hämtar vald frequency från inputen och samlar i values för plottning
            
    if measure in df_inflation['MEASURE'].values:
            input_values.append(measure) # Hämtar vald measure från inputen och samlar i values för plottning

filt_input_values = df_inflation[  # Säkerstället att de valda värdena matchar värdena i motsvarande kolumn i DataFramen df_inflation
     (df_inflation['COUNTRY'].isin([country])) &
     (df_inflation['SUBJECT'].isin([subject])) &
     (df_inflation['FREQUENCY'].isin([frequency])) &
     (df_inflation['MEASURE'].isin([measure]))
 ]

filt_input_values = filt_input_values.drop(columns=['INDICATOR', 'Flag Codes']) # Filtrerar bort kolumner som ej ska användas i plottningen
filt_input_values['Value'] = filt_input_values['Value'].astype(float) # Behövde konvertera om inflationsvärdena till numeriska värden då de var skrivna som strängar

# 5 minsta och 5 högsta värden plockas ut för att plottas med cirklar i diagrammet. Value är kolumnnamnet för inflationen
min_inflation = filt_input_values.nsmallest(5, 'Value') 
max_inflation = filt_input_values.nlargest(5, 'Value')


plt.figure(figsize=(14,7))

# Plottar inflationen för valda values av användare, samt cirklar för minsta och högsta värden
plt.plot(filt_input_values['TIME'], filt_input_values['Value'])  
for index, row in min_inflation.iterrows():
    plt.plot(row['TIME'], row['Value'], 'o', markersize=6, label=f"['{row['TIME']}', 'Minsta']")

for index, row in max_inflation.iterrows():
    plt.plot(row['TIME'], row['Value'], 'o', markersize=6, label=f"['{row['TIME']}', 'Högsta']")

plt.legend(loc='upper right')  # Flyttade upp label till högra hörnet

plt.xlabel('År')
plt.ylabel('Inflation')
plt.title(f'Inflation för {country}, {subject}, {frequency}, {measure}')

# Roterar årtalen på x-axeln
plt.xticks(rotation=80, ha="right")

# Sätter grid och visar diagrammet
plt.grid(True)
plt.show()      


