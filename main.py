import random
import math
import textwrap
import os
from PIL import Image, ImageDraw, ImageFont


input_path = "input.txt"

amount_of_cards = 63

# should be a squared number, e.g 9, 16, 25...

amount_of_entries_per_card = 16

title = ""


def main():

    if not os.path.exists("output"):
        os.mkdir("output")


    with open(input_path, "r") as file:
        possible_entries = file.read().split("; ")

    for i in range(amount_of_cards):
        card_entries = generate_card_entries(possible_entries)
        createCard(card_entries, i)


def generate_card_entries(possible_entries):
    card = []
    duplicates = 0
    while len(card) < amount_of_entries_per_card:
        entry = random.choice(possible_entries)
        if entry not in card or duplicates < 2:
            card.append(entry)
        else:
            duplicates += 1
    return card


def createCard(card_entries, iteration):
    image_height = 1748
    image_width = 2480

    image = Image.new('RGB', (image_width, image_height), color="white")
    title_font = ImageFont.truetype('arial.ttf', 100)
    normal_font = ImageFont.truetype('arial.ttf', 60)
    draw = ImageDraw.Draw(image)

    cell_width = image_width / math.sqrt(amount_of_entries_per_card) - 40 / math.sqrt(amount_of_entries_per_card)
    cell_height = image_height / math.sqrt(amount_of_entries_per_card) - 50
    header_height = 180
    header_width = image_width

    for row in range(int(math.sqrt(amount_of_entries_per_card))):
        for col in range(int(math.sqrt(amount_of_entries_per_card))):
            # Calculate the cell position
            x = col * cell_width + 20
            y = row * cell_height + header_height
            entry = card_entries[int(row * math.sqrt(amount_of_entries_per_card) + col)]
            draw.rectangle((x,y, x + cell_width, y + cell_height), outline='black')

            # wrap entry so it fits the rectangle
            lines = textwrap.wrap(entry, width=int(cell_width / normal_font.getlength("c")))

            total_line_height = __getTotalLineHeight(lines, normal_font)

            # Draw the text in the cell
            for line in lines:
                line_height = normal_font.getbbox(line)[3]
                draw.text((x + cell_width / 2 - normal_font.getlength(line) / 2, y + cell_height / 2 - total_line_height / 2), line, font=normal_font, fill='black')
                y += line_height

    draw.rectangle((20,20, image_width - 20, header_height - 10), outline='black')
    draw.text((header_width / 2 - title_font.getlength(title)/ 2, 30) , title, font=title_font, fill='black')
    image.save(f"output/bingo{iteration + 1}.png", dpi=(300,300))

def __getTotalLineHeight(lines, font):
    sum = 0
    for line in lines:
        sum += font.getbbox(line)[3]
    return sum

if __name__ == "__main__":
    main()
