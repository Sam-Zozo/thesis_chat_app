
import unicodedata
from data_cleaning import is_leet
text = "ᴛᴀɴɢɪɴᴀ"# 𝕥𝕒𝕟𝕘𝕚𝕟𝕒"
text2 = "$#1+"
text3 ='tangina'
print(unicodedata.is_normalized('NFKD',text))
print(unicodedata.is_normalized('NFKD',text3))
print(type(text))
nData = unicodedata.normalize('NFKD', text).encode('utf-8')
print(nData.decode('utf-8'))