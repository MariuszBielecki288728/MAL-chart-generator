from  bs4 import BeautifulSoup

html = """
<div><a href="https://myanimelist.net/manga/103364/Isekai_Mahou_wa_Okureteru" class="hovertitle">Isekai Mahou wa Okureteru! (2016)</a></div>
			<div style="margin-top: 8px;">Felmenia Stingray was a genius magician. She quickly became the most distinguished magician of the Astel Kingdom after her discovery of white fire magic, which had the power to burn anything.

Howev... <a href="https://myanimelist.net/manga/103364/Isekai_Mahou_wa_Okureteru">read more</a></div>
			<div class="spaceit"><span class="dark_text">Genres:</span> Action, Fantasy</div>
			<div><span class="dark_text">Status:</span> Publishing</div>
			<div class="spaceit"><span class="dark_text">Volumes:</span> Unknown
			</div>

			<div><span class="dark_text">Score:</span> 7.05 <small>(scored by 749 users)</small></div>
			<div class="spaceit"><span class="dark_text">Ranked:</span> #8724</div>
			<div><span class="dark_text">Popularity:</span> #3201</div>
			<div class="spaceit"><span class="dark_text">Members:</span> 2,565</div>
"""
soup = BeautifulSoup(html, 'html.parser')
print((soup.find_all('div')[2].span.next_sibling.string)) #soup.get_text().strip().splitlines()[1].strip().split(', ')
