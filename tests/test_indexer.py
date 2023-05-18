import pytest
from podcast_agent.services.indexer import IndexerService

indexer = IndexerService()

text = """
The site of Toronto lay at the entrance to one of the oldest routes to the northwest, a route known and used by the Huron, Iroquois, and Ojibwe, and was of strategic importance from the beginning of Ontario's recorded history.[55]

In the 1660s, the Iroquois established two villages within what is today Toronto, Ganatsekwyagon (Bead Hill) on the banks of the Rouge River and Teiaiagon on the banks of the Humber River. By 1701, the Mississaugas had displaced the Iroquois, who abandoned the Toronto area at the end of the Beaver Wars, with most returning to their homeland in present-day New York state.[56]

French traders founded Fort Rouillé in 1750 (the current Exhibition grounds were later developed there), but abandoned it in 1759 during the Seven Years' War.[57] The British defeated the French and their indigenous allies in the war, and the area became part of the British colony of Quebec in 1763.

During the American Revolutionary War, an influx of British settlers arrived there as United Empire Loyalists fled for the British-controlled lands north of Lake Ontario. The Crown granted them land to compensate for their losses in the Thirteen Colonies. The new province of Upper Canada was being created and needed a capital. In 1787, the British Lord Dorchester arranged for the Toronto Purchase with the Mississaugas of the New Credit First Nation, thereby securing more than a quarter of a million acres (1000 km2) of land in the Toronto area.[58] Dorchester intended the location to be named Toronto.[54] The first 25 years after the Toronto purchase were quiet, although "there were occasional independent fur traders" present in the area, with the usual complaints of debauchery and drunkenness.[55]
"""


class TestIndexerService:
    def test_read_text(self):
        content = indexer.read_from_supabase('episode-audio-files', 'test.mp3')
        print(content)
    
    def test_persist_index(self):
        print(indexer.persist_index(text))

    def test_run_query(self):
        indices = indexer.index_content(text)
        resp = indexer.run_query(indices, "when was Fort Rouillé founded?")
        assert '1750' in resp.response

        