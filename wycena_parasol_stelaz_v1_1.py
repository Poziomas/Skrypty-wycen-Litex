# ========================================================================
# SKRYPT AUTOMATYCZNEJ WYCENY STELAŻY PARASOLI v1.1
# ========================================================================
# 
# Autor: Kamil Jabłoński
# Data: 2025-06-06 14:30
# Sprawdził: Michał Węgrzynek
# Wersja: 1.1 - obejmuje linie Atlantic, Classic, Easy Up, Harmony, Ibiza Plus, Telescopic
# Zmiany v1.1: Poprawiono logikę wyboru koloru malowania i anodowania, usunięto farby proszkowe, usunięto robociznę malarni W18, dodano zabezpieczenie przed wartościami ujemnymi
# 
# Opis: Skrypt oblicza cenę sprzedaży stelaży parasoli 
# ========================================================================

# ========================================================================
# SKRYPT AUTOMATYCZNEJ WYCENY STELAŻY PARASOLI v1.1
# ========================================================================
# 
# Autor: Kamil Jabłoński
# Data: 2025-06-06 14:30
# Sprawdził: Michał Węgrzynek
# Wersja: 1.1 - obejmuje linie Atlantic, Classic, Easy Up, Harmony, Ibiza Plus, Telescopic
# Zmiany v1.1: Poprawiono logikę wyboru koloru malowania i anodowania, usunięto farby proszkowe, usunięto robociznę malarni W18
# 
# Opis: Skrypt oblicza cenę sprzedaży stelaży parasoli 
# ========================================================================
poprawić tak aby skrypt zwracał cenę 0 gdy wstępje gdziekolwiek value ujemne   

def safe_price_factor(key, default=0):
    """
    Pobiera czynnik ceny z zabezpieczeniem przed wartościami ujemnymi
    """
    value = price_factors.get(key, default)
    return max(0, value) if value is not None else default

def safe_price_component(key, default=0):
    """
    Pobiera składnik ceny z zabezpieczeniem przed wartościami ujemnymi
    """
    value = price_component(key) or default
    return max(0, value) if value is not None else default

def calculate_parasol_frame_price():
    """
    Główna funkcja kalkulacji ceny stelaża parasola
    """
    
    # ====================================================================
    # SEKCJA 1: KURSY WALUT I CZYNNIKI PODSTAWOWE
    # ====================================================================
    skorygować na funkcję get, a nie safe dla wszystjkich czynników ceny
    log("=== ROZPOCZĘCIE KALKULACJI CENY STELAŻA PARASOLA ===")
    
    # K1. Kurs EUR -> PLN
    eur_pln_rate = safe_price_factor("Kurs EUR [PLN]")
    log("Kurs EUR [PLN]: %s" % eur_pln_rate)
    
    # ====================================================================
    # SEKCJA 2: MATERIAŁY PODSTAWOWE
    # ====================================================================
    
    # M1. ALUMINIUM
    aluminum_weight = safe_price_component("Waga aluminium [kg]")
    aluminum_unit_price = safe_price_factor("Cena aluminium surowego [EUR/kg]")
    aluminum_cost = aluminum_weight * aluminum_unit_price * eur_pln_rate
    
    log("--- ALUMINIUM ---")
    log("Waga aluminium [kg]: %s" % aluminum_weight)
    log("Cena aluminium surowego [EUR/kg]: %s" % aluminum_unit_price) 
    log("Koszt aluminium [PLN]: %s" % aluminum_cost)
    
    # M2. STAL
    steel_weight = safe_price_component("Waga stali [kg]")
    steel_unit_price = safe_price_factor("Cena stali [EUR/kg]")
    steel_cost = steel_weight * steel_unit_price * eur_pln_rate
    
    log("--- STAL ---")
    log("Waga stali [kg]: %s" % steel_weight)
    log("Cena stali [EUR/kg]: %s" % steel_unit_price)
    log("Koszt stali [PLN]: %s" % steel_cost)
    
    # ====================================================================
    # SEKCJA 3: WYKOŃCZENIE POWIERZCHNI
    # ====================================================================
    # Odczytanie parametru koloru powłoki
    coating_color = av("Kolor stelaża") or ""
    
    log("--- WYKOŃCZENIE POWIERZCHNI ---")
    log("Kolor stelaża: %s" % coating_color)
    
    # Zabezpieczenie - inicjalizacja kosztów
    coating_cost = 0
    
    # MALOWANIE PROSZKOWE
    if "farba proszkowa" in coating_color:
        painting_surface = safe_price_component("Powierzchnia malowania [m2/szt]")
        log("MALOWANIE PROSZKOWE - Powierzchnia [m2/szt]: %s" % painting_surface)
        paint_price = 0

        if "biały RAL 9016" in coating_color:
            paint_price = safe_price_factor("Cena malowania proszkowego na biało RAL 9016 [PLN/m2]")
            
        elif "czarny RAL 9005" in coating_color:
            paint_price = safe_price_factor("Cena malowania proszkowego na czarno RAL 9005 [PLN/m2]")

        elif "antracyt RAL 7021" in coating_color:
            paint_price = safe_price_factor("Cena malowania proszkowego na szaro RAL 7021 [PLN/m2]")
            
        elif "szary RAL 9022" in coating_color:
            paint_price = safe_price_factor("Cena malowania proszkowego na szaro RAL 9022 [PLN/m2]")
        else:
            log("UWAGA: Nie rozpoznano koloru farby proszkowej!")

        coating_cost = painting_surface * paint_price
        log("Malowanie: %s, Cena [PLN/m2]: %s, Koszt [PLN]: %s" % (coating_color, paint_price, coating_cost))
            
    # ANODOWANIE
    elif "anodowany" in coating_color:
        anodizing_surface = safe_price_component("Powierzchnia anodowania [m2/szt]")
        log("ANODOWANIE - Powierzchnia [m2/szt]: %s" % anodizing_surface)
        
        if "czarny C-35 anodowany" in coating_color:
            anodizing_price = safe_price_factor("Cena anodowania C-35 czarny [PLN/m2]")
            coating_cost = anodizing_surface * anodizing_price
            log("Wybrano anodowanie czarny C-35, Cena [PLN/m2]: %s, Koszt [PLN]: %s" % (anodizing_price, coating_cost))
            
        else:
            log("UWAGA: Nie rozpoznano typu anodowania!")
            
    # ZABEZPIECZENIE
    else:
        if coating_color:
            log("BŁĄD: Nie rozpoznano typu wykończenia powierzchni: %s" % coating_color)
        else:
            log("BŁĄD: Brak informacji o kolorze powłoki!")
    
    log("--- KOSZT POWŁOKI [PLN]: %s ---" % coating_cost)
    
    # ====================================================================
    # SEKCJA 4: ROBOCIZNA - STANOWISKA PRACY
    # ====================================================================
    
    log("--- ROBOCIZNA ---")
    
    # R1. Przygotowanie montażu W1
    work_time_w1 = safe_price_component("Czas pracy Przygotowanie montażu W1 [min]")
    work_rate_w1 = safe_price_factor("Cena robocizny Przygotowanie montażu W1 [PLN/godz]")
    work_cost_w1 = work_time_w1 * work_rate_w1 / 60
    log("Czas pracy W1 [min]: %s, Stawka [PLN/godz]: %s, Koszt W1 [PLN]: %s" % (work_time_w1, work_rate_w1, work_cost_w1))
    
    # R2. Montaż W6
    work_time_w6 = safe_price_component("Czas pracy Montaż W6 [min]")
    work_rate_w6 = safe_price_factor("Cena robocizny Montaż W6 [PLN/godz]")
    work_cost_w6 = work_time_w6 * work_rate_w6 / 60
    log("Czas pracy W6 [min]: %s, Stawka [PLN/godz]: %s, Koszt W6 [PLN]: %s" % (work_time_w6, work_rate_w6, work_cost_w6))
    
    # R3. Montaż Ibiza W7
    work_time_w7 = safe_price_component("Czas pracy Montaż Ibiza W7 [min]")
    work_rate_w7 = safe_price_factor("Cena robocizny Montaż Ibiza W7 [PLN/godz]")
    work_cost_w7 = work_time_w7 * work_rate_w7 / 60
    log("Czas pracy W7 [min]: %s, Stawka [PLN/godz]: %s, Koszt W7 [PLN]: %s" % (work_time_w7, work_rate_w7, work_cost_w7))
    
    # R4. Tokarnia W8
    work_time_w8 = safe_price_component("Czas pracy Tokarnia W8 [min]")
    work_rate_w8 = safe_price_factor("Cena robocizny Tokarnia W8 [PLN/godz]")
    work_cost_w8 = work_time_w8 * work_rate_w8 / 60
    log("Czas pracy W8 [min]: %s, Stawka [PLN/godz]: %s, Koszt W8 [PLN]: %s" % (work_time_w8, work_rate_w8, work_cost_w8))
    
    # R5. Ślusarnia W10
    work_time_w10 = safe_price_component("Czas pracy Ślusarnia W10 [min]")
    work_rate_w10 = safe_price_factor("Cena robocizny Ślusarnia W10 [PLN/godz]")
    work_cost_w10 = work_time_w10 * work_rate_w10 / 60
    log("Czas pracy W10 [min]: %s, Stawka [PLN/godz]: %s, Koszt W10 [PLN]: %s" % (work_time_w10, work_rate_w10, work_cost_w10))
    

    
    # ====================================================================
    # SEKCJA 5: DODATKI
    # ====================================================================
    
    # D1. Dodatki do stelaża
    accessories_cost = safe_price_component("Wartość dodatków do stelaża parasola [PLN/szt]")
    log("--- DODATKI ---")
    log("Wartość dodatków do stelaża [PLN/szt]: %s" % accessories_cost)
    
    # ====================================================================
    # SEKCJA 6: OŚWIETLENIE
    # ====================================================================
    
    # D2. Oświetlenie wbudowane
    lighting_cost = safe_price_component("Oświetlenie wbudowane [PLN/szt]")
    log("--- OŚWIETLENIE ---")
    log("Oświetlenie wbudowane [PLN/szt]: %s" % lighting_cost)
    
    # ====================================================================
    # SEKCJA 7: OPAKOWANIE
    # ====================================================================
    
    # D3. Opakowanie jednostkowe
    packaging_cost = safe_price_component("Opakowanie jednostkowe [PLN/szt]")
    log("--- OPAKOWANIE ---")
    log("Opakowanie jednostkowe [PLN/szt]: %s" % packaging_cost)
    
    # ====================================================================
    # SEKCJA 8: PODSUMOWANIE KOSZTÓW PODSTAWOWYCH
    # ====================================================================
    
    # Suma wszystkich kosztów bezpośrednich
    direct_costs = (aluminum_cost + steel_cost + coating_cost +
                   work_cost_w1 + work_cost_w6 + work_cost_w7 + 
                   work_cost_w8 + work_cost_w10 +
                   accessories_cost + lighting_cost + packaging_cost)
    
    log("--- KOSZTY PODSTAWOWE ---")
    log("Suma kosztów bezpośrednich [PLN]: %s" % direct_costs)
    
    # ====================================================================
    # SEKCJA 9: KOSZTY WYDZIAŁOWE
    # ====================================================================
    
    departmental_rate = safe_price_component("Koszty wydziałowe [%]")
    departmental_cost = direct_costs * departmental_rate / 100
    
    log("--- KOSZTY WYDZIAŁOWE ---")
    log("Koszty wydziałowe [%%]: %s" % departmental_rate)
    log("Koszty wydziałowe [PLN]: %s" % departmental_cost)
    
    # ====================================================================
    # SEKCJA 10: KOSZT CAŁKOWITY
    # ====================================================================
    
    total_cost = direct_costs + departmental_cost
    log("--- KOSZT CAŁKOWITY ---")
    log("Koszty razem [PLN]: %s" % total_cost)
    
    # ====================================================================
    # SEKCJA 11: MARŻA I CENA SPRZEDAŻY
    # ====================================================================
    
    margin_rate = safe_price_component("Marża handlowa PLN [%]")
    selling_price = total_cost / (100 - margin_rate) * 100
    
    log("--- MARŻA I CENA KOŃCOWA ---")
    log("Marża handlowa [%%]: %s" % margin_rate)
    log("CENA SPRZEDAŻY [PLN]: %s" % selling_price)
    
    log("=== ZAKOŃCZENIE KALKULACJI ===")
    
    return selling_price


# ========================================================================
# WYWOŁANIE GŁÓWNEJ FUNKCJI
# ========================================================================

# Uruchomienie kalkulacji ceny stelaża parasola
price = calculate_parasol_frame_price()