import streamlit as st
import pandas as pd
import time
import json

#hide sidebar


# Načtení uživatelů ze souboru spravce.json
with open("spravce.json", "r", encoding="utf-8") as f:
    uzivatele = json.load(f)

# Inicializace session state
if "prihlasen" not in st.session_state:
    st.session_state["prihlasen"] = False # Status přihlášení uživatele
if "jmeno" not in st.session_state:
    st.session_state["jmeno"] = None # Jméno přihlášeného uživatele
if "email" not in st.session_state:
    st.session_state["email"] = None # Email přihlášeného uživatele


# Pokud je status přihlášení False (Nepravda), zobrazí se formulář pro přihlášení
if not st.session_state["prihlasen"]:
    st.markdown(
    """
    <style>
        .st-emotion-cache-1itdyc2 {
            visibility: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True
)
    # Formulář pro přihlášení
    with st.form("prihlaseni", clear_on_submit=True):
        prihlasovaci_jmeno = st.text_input("Přihlašovací jméno:")
        heslo = st.text_input("Heslo:", type="password")

        # Proces přihlášení
        if st.form_submit_button("Přihlásit se", use_container_width=True):

            # Podíváme se přes for loop na každého uživatele v json souboru a zkontrolujem, zda se zadané přihlašovací jméno a heslo nachází shoďují s některým uživatelem
            for uzivatel in uzivatele["uzivatele"]:
                # Pokud najdeme shodu, tak uložíme jméno a email uživatele do session state, změníme status přihlášení na True a přerušíme smyčku přes break, protože už nemá cenu hledat dál
                if prihlasovaci_jmeno == uzivatel["prihlasovaci_jmeno"] and heslo == uzivatel["heslo"]:
                    st.session_state["jmeno"] = uzivatel["jmeno"]
                    st.session_state["email"] = uzivatel["email"]
                    st.session_state["prihlasen"] = True
                    break
            # Pokud je status přihlášení True (Pravda), zobrazí se zpráva o úspěšném přihlášení a aplikace se restartuje
            if st.session_state["prihlasen"]:
                st.success("Přihlášení proběhlo úspěšně.")
                time.sleep(3)
                st.rerun()
            # Pokud je status přihlášení False (Nepravda), zobrazí se chybová zpráva
            else:
                st.error("Špatné přihlašovací údaje.")
                
# je prihlasen  
        

if st.session_state["prihlasen"]:
    
#hide sidebar
    st.markdown(
    """
    <style>
        .st-emotion-cache-1itdyc2 {
            visibility: show;
        }
    </style>
    """,
    unsafe_allow_html=True
)
    st.header("Vítejte na stránce skladu")
    
    st.header("Skladové zásoby")

# nacteni sklacu z cvs a zobrazeni polozek dle nazvu s moznosti editace vsech parametru polozky
    sklad = pd.read_csv("data.csv")
    st.dataframe(sklad)
    st.write("")

#zobrazeni polozky dle kategorie
    st.header("Zobrazení položky dle kategorie")
    kategorie = st.selectbox("Vyber kategorii", sklad["kategorie"].unique())
    # serazeni polozek v kategorii dle abecedy
    sklad = sklad.sort_values(by="nazev")
    st.dataframe(sklad[sklad["kategorie"] == kategorie])
    st.write("")    
    

#vyber kategorie, vyber polozky a editace parametru polozky
    kategorie = sklad["kategorie"].unique()
    vyber_kategorie = st.selectbox("Vyber kategorii", kategorie, key="editace_polozky")
    polozky = sklad[sklad["kategorie"] == vyber_kategorie]["nazev"].unique()
    vyber_polozku = st.selectbox("Vyber polozku", polozky)
    editace = st.checkbox("Editace parametru polozky")
    if editace:
        polozka = sklad[(sklad["kategorie"] == vyber_kategorie) & (sklad["nazev"] == vyber_polozku)]
        mnozstvi = st.number_input("pocet", value=int(polozka["pocet"]), min_value=0)
        cena = st.number_input("cena", value=int(polozka["cena"]), min_value=0)
        if st.button("Ulozit"):
            sklad.loc[(sklad["kategorie"] == vyber_kategorie) & (sklad["nazev"] == vyber_polozku), "počet"] = mnozstvi
            sklad.loc[(sklad["kategorie"] == vyber_kategorie) & (sklad["nazev"] == vyber_polozku), "cena"] = cena
            sklad.to_csv("data.csv", index=False)
            st.success("Parametry položky byly upraveny.")
            time.sleep(3)
            st.rerun()
            
# pridani nove polozky dle kategorie a parametru kategorie, nazvu, poctu a ceny
    st.header("Přidání nové položky")
    kategorie = st.selectbox("Kategorie", sklad["kategorie"].unique())
    nazev = st.text_input("Název")
    pocet = st.number_input("Počet", min_value=0)
    cena = st.number_input("Cena", min_value=0)
    if st.button("Přidat"):
        pridana_polozka = pd.DataFrame({"id":[len(sklad)+1],"kategorie": [kategorie], "nazev": [nazev], "pocet": [pocet], "cena": [cena]})
        st.write(pridana_polozka)
        pridat = pd.concat([sklad, pridana_polozka], ignore_index=True)
        pridat.to_csv("data.csv", index=False)
        st.success("Položka byla přidána.")
        time.sleep(3)
        st.rerun()
        
# smazani polozky dle kategorie a nazvu
    st.header("Smazání položky")
    kategorie = st.selectbox("Kategorie", sklad["kategorie"].unique(),key="smazani_polozky")
    nazev = st.selectbox("Název", sklad[sklad["kategorie"] == kategorie]["nazev"].unique(), key="smazani_polozky1")
    if st.button("Smazat"):
        sklad = sklad[(sklad["kategorie"] != kategorie) | (sklad["nazev"] != nazev)]
        sklad.to_csv("data.csv", index=False)
        st.success("Položka byla smazána.")
        time.sleep(3)
        st.rerun()
# odhlaseni uzivatele

    st.header("Odhlašení")
    if st.button("Odhlásit se"):
        st.session_state["prihlasen"] = False
        st.session_state["jmeno"] = None
        st.session_state["email"] = None
        st.success("Odhlášení proběhlo úspěšně.")
        time.sleep(3)
        st.rerun()
        

