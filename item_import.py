import pandas as pd
items_list = pd.read_excel("items_list.xlsx")


def item_pools():
    """
    Gibt dictionary mit item_pools_liste zurück, basierend auf rarity der Items"""

    item_pools = {
        "common": [],
        "uncommon": [],
        "rare": [],
        "epic": [],
        "legendary": []
    }

    for index, row in items_list.iterrows():
        rarity = row['rarity']

        if rarity in item_pools:
            item_pools[rarity].append(row.to_dict())
        else:
            print(f"Warnung: Unbekannte Rarity '{rarity}' für Item '{row['name']}'")

    return item_pools

"""können wir mit der Implementierung von space x und space y warten --> größe von Sprite durch img.get_rect()
und derzeit habe ich Itemslot als Group mit die eine Sprite halten kann, muss mir dafür neue Implementierung überlegen"""


"""
pools = item_pools()
total_in_pools = sum(len(v) for v in pools.values())
total_in_excel = len(items_list)

print(f"Items in Excel: {total_in_excel}")
print(f"Items in pools: {total_in_pools}")

if total_in_pools != total_in_excel:
    print("Achtung: Nicht alle Items wurden zugeordnet!")

print("Holzschwert" in pools["uncommon"])

"""

