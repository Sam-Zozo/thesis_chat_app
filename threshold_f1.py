import time
import compare
from jaro_winkler import jaro_Winkler
import json
from data_cleaning import *
raw_profanity = [
"amputa",
"bilat",
"binibrocha",
"bobo", 
"bogo",
"boto",
"brocha",
"burat",
"bwisit",
"demonyo",
"engot",
"gago",
"hayop",
"hinayupak",
"hudas",
"iniyot",
"inutil",
"iyot",
"jakol",
"kagaguhan",
"kantot",
"kantutan",
"kaululan",
"kike",
"kikinginamo",
"kingina",
"kupal",
"leche",
"lintik",
"nakakaburat",
"olok",
"pakingshet",
"pakshet",
"pakyu",
"pokpok",
"pucha",
"puchanggala",
"puchangina",
"puke",
"pukinangina",
"punyeta",
"puta",
"putangina",
"putaragis",
"ratbu",
"shunga",
"siraulo",
"suso",
"tae",
"taena",
"tamod",
"tanga",
"tangina",
"taragis",
"tarantado",
"timang",
"tite",
"tungaw",
"ugok",
"ulol",
"ungas",
"ungol"
]
raw_profanity.sort()
# print(' '.join(raw_profanity))

first = '4mPut4 b!L4T b!N1br00kh@ bObO 806o bo70 Br0cha BurAt 8w1SI7 d3munY0u 3ng0T g46ui h4yOP HinaYUp4c ḫUdas 1n!Y0T |nUtil iYO7 jacuL CaG4guH4n k4n70T K4NtUt4nn c4ululAn cYke c!k!Ng1n@mO cYgnGYnyA kUPAl l3cḧ3 l1NTik naK4cAbura7 0LoK paKYnG5h3T Pakzh37 p4cyU P0Cp0C pUCha PuChAńG64la pUchAgnGIna puC3 PUkin4gnG|n4 puNY3ta PUTa puTangiNA pUt4ragiZ raT8U SHUnGa s1R4ulᴏ 5U50 T43 ta3ṋ4 t4m0dd 74gnG4 t4nGiN4 t4R46|z taR4n7@do 7!m@ng 7|t3 7uNGaw Ug*K ulOL unG4s ugn60L'
second = 'ampUT4 bil4t binibr0ch4 b0b0 b0g0 b0t0 br0ch4 bur4t bwisit d3m0ny0 3ng0t g4g0 h4y0p hin4yup4k hud4z iniy0t inutil iy0t j4k0l k4g4guh4n k4nt0t k4ntut4n k4ulul4n kik3 kikingin4m0 kingin4 kup4l l3ch3 lintik n4k4k4bur4t 0l0k p4kingsh3t p4ksh3t p4kyu p0kp0k puch4 puch4ngg4l4 puch4ngin4 puk3 pukin4ngin4 puny3t4 put4 put4ngin4 put4r4giz r4tbu shung4 sir4ul0 sus0 t43 t43n4 t4m0d t4ng4 t4ngin4 t4r4giz t4r4nt4d0 tid00dg tit3 tung4w ug0k ululz ung4z ung0l'
third = '@mpuT4 b|1aT B|ň!BrỎcẖ4 bObỎ bu6Ỏ 8ỎTØ BrOch4 Bur4T bWYsYT D3mm0ny0 ENG0T 6AG0 hay0P hYN@yup4k hUD@z 1ṇ|Y07 |ɲu7|l |y07 ;AKo1 C@G46U#Agn CANT0T k4n7uT4gn caUlu1AN C1cE kiCYɲgYn@m0 cYɲg1ɲa cup@l l3Ch3 l1n7|k nAC4KaBurat 0l0C p4K1NgZHet p@KshEt pakYu PocP0K Pukhh4 PUkh@Ngg@L4 PUkȟ4ṅGIna PUC3 pucIgn4nGYnA Punye74 puta pUT4N6ign4 PU7aRag!S ratbU ShunGa zIraUl0 Su50 Ta3 T43n4 7@M0d 74gnga t4nGin@ 7@rAgYs 7Ar4gnT4ḍő TimaN6 TY7e TUng@w u60k Ul0l unGa5 ung0L'
forth = '@4mpU7a B11@T 8INIBrouChA 80bhu B0goh b0t0 BrOcẖA Burat bWizit DemỎNy0 3nGot gAgo hay0P H1ṇ4yuPAC Hud@z 1ṇiY07 InU7Y1 |y07 ;acol kAGaGuh4n k4nt07 K4ñtuot4n c4ulu1An kYke kIKYgngi₪amO CYNGIgn4 KUpAl LECħ3 L|ɲt|c nak@k4bur4t 0l0k pakInGZH3T PaCSh3t PAcYu PòCPōC pukhA PUcȟ4ngG414 puCh@nGinA PuCe PucYnangIn4 Puṅy3ta PutA Putan6Iṅa Put4R@g!z Ra7bU sHun64 Z|RauL0 ZU5O 7@3 Ta3nA T4M0d 7@Nga 74ṅṅgin@ TaR4GY5 TAr4n7@ḋő 71M4Ng 7i7E 7uNg@w uG0C UlőL uNGAS unG01'
fifth = '4MPU74 b!147 binYbRuocH@ b0bO b0gu bh0t0 BRokh4 buRat BW!z|7 d3monYớ eN6Ơ7 g4G0 h@Y0P Ⱨ!ɲ@yUp4K #UDas ign|yot !gnUt11 |y0t ;aC0l K4g4guħ4ññ c4ɲtOT K@gnTuTAn C4UluL4ññ k|Ce c!cin6iNAm0 KYngYN4 KuP41 LEkħħE l1N7iK NaKakABURAT o10c p4C!ngzH3T PacSh3T p4KYU P0cPòc PuCha pukHAn6GAl4 pUkȟ4gngYgn@ pUK3 Pukin4ngIṅ4 pugnYEtA pUTa Pu7agngYgnA PU74R4g1z r4tBU SHUnGA Z|r4Ul0 suso tA3 Ta3na 7Am0oD 7@Ng4 T4ṅGYṅ4 taR46Ys t@r4ntad0 t|ᵯ4n6 7It3 tUn64hw UgőC Ulo1 UhnG4Z UNGőoL'


sixth ='4mPuTa 81l4t B!n!brocH4 8oB0 bàGO Bø70 bR0čh4 bUR4T bwiz17 d3m()nyO 3nGô7 gaGõ H4yóp hìń4YUp4K Hûd45 1nïy07 1nU7!l !yO7 J4C0l k4gágUHAñ kåñto+ k4ñ7ütân C4u|u14n k1ce c!c!nGYn@m0 c!Ng1n4 cupaL 13čh3 l|n7icc n@KAC@bUR@t O1OK P4CIgnGZhE7 PakS]-[Et paCyu p0CpoC pUçha PUćh4nGG4|4 puçh4ñ6|na pUce PuKin@nGYn4 PUnyE7@ PU74 PuT4ngIn4 PUtaR4615 rAtBU zHUn16a zIR4ulo 5U5o 7Ae Tá3ñA t@môd 7@NGa 7Añg|na T4r4g!Z taR4nt4D0 Tim4Ng TI733 7un64w u60K Ul0l un64z un60l'
seventh = '@Mpu7@ b!14t B!gnIbR0kHa BOb() Bog() 8Oto br0kh4 buR4t bW151t d3m()ny0 Egng0T g4g() h4yOP h|n4YuP4k HUDAz YN!y0T |nUt!L |yoT ;@Kol k4g@guh4n CanT0t canTutaN KaU1Ul4gn C1Ce c!kIgnGYnAm0 cYn61N@ cUPAL 13kh3 LYNt|c næKak48URat ô10k P4K|ngZH37 P4kSHe7 pacyU p0kpOC pUkh4 pukH4Ngg41a pUkhAng1n4 pUc3 pùCin4nG|gn4 PUnyEta PUT4 PU7@m6!Na PUt@Ra6Ys ratbU 5hUn6ã S!r4U10 5us0 T43 7aENA Támo|) tæńg4 T4n6!n4 T4r4Gis 7aR4nT@Do 7!m4gn6 TIt3 tun6āw U6Ok Ul0l Un6Az uNg0L'
eight = 'AMpuTa b!14t B!gnIbR0kHa BOb() Bog() 8Oto br0kh4 buR4t bW151t |)3môny0 Egng0T g4g() h4yOP h|ñ4YuP4k HUDAz YN!y0T inUt!L |yoT ;@Kol k4g@guh4nn CanT0t canTutaN KaU1Ul4gn C1Ce c!kIgnGYnAm0 cYn61N@ cUPAL 13kh3 LYNt|c naK@k48URa+ ó10k P4K|ngZH37 P4kSHe7 pacyU p0kpOC pUkh4 pukH4Ngg41a pUkhAng1n4 pUc3 fUCin4nG|gn4 PUnyEta PUT4 PU7@ñ6!Na PUt@Ra6Ys ratbU zhUń64 S!r4U10 5us0 T43 7aENA Tamo|) +4nG4 T4n6|n4 T4r4Gis 7aR4nT@Do 7!m4gn6 TIt3 tunn6aw U6Ok Ul0l Un6Az uNg0L'
nineth = '@MpuTA bYla7 binībRočha 8O8() b060 80t0 8RõCh4 bur@t 8W|sYT dEm0ny() 3ng0+ g460 H@Y0P hYn@yuP4K hU|)4S Iñ1Y0T !nU7y\ IY()t ;4k01 k@g4GUh4n c4nT()T C@ń7ut@nn c4u1U14n c!c3 k1k|gn6Ygn4m0 C!ng1gn4 kUP41 1Ekhé 1|Nt1K nAC@c4bUR@7 0loc P4c!ñgzh37 p4kZh37 PAkyU p0kP0k puCH4 pUc]-[AnG64L4 pukh4gng!gn@ Puk3 puk1n@ñ61gna PUńY3t4 pUt4 pUT@gn6!NA pu74R@6y5 R47bu Zhung4 zYr4uL0 ZuZoo tà3 T43GgnA 74m0d 74GNG4 t@gnG!ńa 74rag1S 74RańT4d0 t!m4n6 T|7e 7uńG4w uG0k UL01 Ung45 vn601'
tenth = 'AMpU74 8Y1aT b!nYBROkH4 bOb0 B()6o BOT0 bRokhA buRa7 bWYzit d3møNyO enG07 ga60 h4yöp h1NAYvP@k HUdAAS !n!Y()T iNnUtIl iy0T ;@ko1 k4g46Uh4N kaNt0t c4ntUt@n C4UluLAgn CIcE CIk1n6Im4m0 k|ng1ñ@ kUPaL L3kh3 1|n7ic naCak@8uRat OL0c PAKingzh3+ p4CShe7 P4kYU p0cP0k pukH4 pUCh4nGG4L4 pUChaNgINA PuKE PuCIgn@nG1n4 PUnYe7a Put4 puTagng!gn4 pUT@R@6YS raTBu zhunga S|r4Ulo suzO T43 ta3n4 tamm0D tanGa t4ngin4 TAr@GYZ T4rAgn7@dO T!M4ng tit3 7ugnGaw UG0c ULo1 UNg4S ugn6OL'
a11 = 'ampU7a bil@7 b1ñ!br0Cha b0bô 80G0 bô70 brøkH@ 8Ura7 BШiS|T dEmΩnyO eNg0t g46ø ȟ@Y0P h‡n4YuPaK hUd4Z 1Y0t YnU7Y1 |Y07 ;aKø1 c4g4guh@n caNTö7 cAN7uT@n C4ulULAN KYC3 c|C|ngInamO C!ng!gn4 cuP@1 lEch3 LiNTYK gn@C@cAbUR@7 01òc p4C!Ngsh37 Paczhe7 PakYu PōKP0c PUch@ PUkh4ngg4La pUkh4Ng1Na PUC3 PUC1n4ń6|na PUNYE7@ PuT4 PU74gng!N@ PuT4R46is R4T8U 5HuñG4 5iR4U1O sUs0 t@3 ta3na 7AmOd tagnga tañ6!Na T4r4g|5 t4r@nt4D0 71m4nG 71t3 7un64w ugœk ul01 UnGaz Un60L'
a12 = 'AmpU7@ b1l@t b!NY8r0Ch@ Bobo B0go B0t0 bRokȟ@ bURa7 bw!Zit d3M0nyõ eń60T gag0 ȟ@Y0p HiN4yUpAk ȟuÐaS !ń|y0T ińu7Y1 |Y07 j4Ko1 K46@gUh4N k4nT07 canTuT4n K@ulul4N c!K3 kikIN6|NAm0 C!nG!N4 cUpal l3CH3 L!NtIk ń4k4KabURat 0lokk paK|Ng5h37 P4cShET p4kYU P0cP0C PuCha PUcH@nGg4la pukHaNgIn4h PukEh Puk|n@ñG1ńa PuNY3T4h Put4 pUTaNgINa PUt4R@GIS Ra7bU zhUng@ s1r4Ulo ZuZ0 ta3 743n4 7aM0D TAng@ TangIN4 taR@6|s t4r4nT4d0 T|m@Ng TI73h 7Ung4w UgøC uLøL UngaZ Ung0L'
a13 = '4mpu7@ b|LA7 BIni8R0ch@ bOB0 b0g0 bo7ø bRõcha buR@7 8wIz1t deM0ńyo 3ñgoT GaG0 h4Y0p #Yñ4YUpaC huÐa5 INYYO7 1NUT1L |YOT jaCo1 ca646u#4gn cAN70t C4n7Ut4N c4uLuLAN c|Ke C|cYn6!N4mõ c1ngYN4 CUPa1 lekH3 liN7Yc nacACaBuR@7 õl0k P@K1NgSH3T pAcShET p4cYu p0Cpók pUCȟ4 PUCh@N66@1A pukhAńGYń4 pUK3 pUKYgnañgin4 pugnY37A puTa puT4ngYN4 put4R@gYZ R4TbU SHUng4 5!r4ul0 sU50 t43 tA3na Tàmõð T4N6a T4n6!n4 tArAgIz 7@R4ńTadO TimanG TIt3 7un6@w u6ök uL01 uNG4s un601'
a14 = '@mPU74 b1l4T b!ńYBRokH@ BōBó 80gô B07ô bRocHa 8Ura7 8Шi5YT d3M0nYo 3ng0T 64gö H4YoP h!gnAYupac ḣUd4z INiYO7 Y₪UTiL iY07 JaKO1 Ka6agUh4N kanT07 k4ntut@n kAuLuLAN kic3 kIC|NG!NaMu ciNG!n4 CuPAL l3ch3 1!nt|C nac@K48urat 0LoK pAkiNgzHe7 p@KZhEt P4CYu PokPoKk PuCha PUChangg4La pUch4NGińA PUcE pUc|gn4n6iNA PUNY37a pUt@ pUtanGIna puTaR4G!z R4t8U 5hUNGA SIr4ulo zUZ0 ta3 t43na tam0d t@ngA 7ańGIńa tarAgIz taRanT4D0 T!m4ng T|te tUnG4W uGoK ul0l Ung4z Uńg0l'
a15 = 'amPUT@ b!147 BinY8RokH4 bO80 8OG0 b070 brokh4 bUR4T bw1S|T Ḋ3M0Ny0 En6o7 g4g0 h4YoP hInayUP4k huḊ4S !NYY0t 1gnu7i1 1yoT j4C0L ka6aguH@gn c4NT07 c4gntuTAn c4ULuL4n CYc3 CYc|n6iN4mO kIn6!NA CuPAL l3CH3 l!nT|k gnAk4C@bURaT 0L0k p4kingshEt P4cSH3t P@cyU P0KP0K puch4 Puch4nG6ala PUkhAgng!n4 PUce pUKYNAng!nA pugny3T@ pu74 PUT4nG!ń@ PU74RaGYZ R47BU ShUnga zYrAuL0 5uso 743 743gna tAm0Ḋ T@nga tańG1gn4 taraG|Z 7ARant@DO 7|MaNG 7|te tUn64w U60c Ul0L uNG45 ungo1'
a16 = '@mpU7a b1l4T b|N1Br0kh4 b0b0 b0GO b070 8roCha bUR4T BwY5YT d3M0gnYO En6oT g4go h4yoP hiNayupAk HUD@Z INIy0t 1nU7Y1 Yy0T j4c0l ca6A6UHan c4NT0t C4N7U74N k@ulUL4n KiC3 CIkYnGinaMo cYngiN@ kuPA1 L3CH3 LYnT1C n4c4k4bUr4t 0l°K P4cigngZh37 pAk5HEt pacyU poCp0k PUkHA Puch4ngG4L@ PUch4nG!24 PukE pUk|n4n6Yna PUgny3Ta Pu7a PUTa2G|Na PutaragIZ r4TBU S4Un6a s!r4uL0 zus0 743 TAena T@mOd 7aNG4 7aNgi#4 tar4gI5 t4r42TAd() t|M4nG 7!73 7unGAW uGoc Ul0L unGaZ ugng9l'
a17 = '4mput4 b1lat B|r|bR0c#a Bob* bogO boto Br9C4a 8Ur47 8w|zIT d3mOgnyo 3nGo7 6ag0 h@Y0p #InayuPak hu|)aS 1n!y0T !nuTIL iy0t j4kOl kagAguh4|\| c4|\|707 C4n7utan C4u1Ulan C!Ce c|K1|\|G1N4M0 CINgIgn4 Kup@1 L3ch3 L!nTIC nacac4buR4T oLOK pAC!ngSh3t P4ks#et P@CYU p0KP0k puCh4 Puc4anG6a1a PukHarg!n@ PuC3 puK|?@n6I2a PUñYetA puta pUT4nG!n4 PUTaRAgY5 R478u 5hun64 ZIRau1O 5UsO 7Ae 743NA t@M*Ð TAng4 7aN6YN@ tar4g!s t4RaNt@d0 t1Mańg 7|t3 Tu2g4w UG0k ul0L Ung4Z uńg°1'
a18 = 'AmPu74 b1l@T b!N|broCh4 B0b° 8069 b0t0 bRok#4 8ur@T BµYzIT đ3M0Ny0 3n60T g4gO H@y0P hYNaYUPAK #UÐA5 inIyøt inu71l 1y0t ;4col Kag4Guh4N k4Nt0t KagntUT4n caulU1@N cYcE cicYngIgn4mo kiN6Iµa KuP4l 1EkhE lYNt|c n4k4k4bur4t O10c paC!gn6Zh3t P4CShET paKYU P0KP0K pUkh4 PUc4An6g4l4 pukhAngY2A Puc3 Puc|µang!Na PUnY374 pU74 Pu74n6InA PUt@RagYS Ra7bu zhunga s|r4u10 SuSo T@E T@eń4 T4m0Ð 74µgA 74NgIn4 taR46IS 7aRANtađ0 7imAń6 tiT3 TUNg4W ugOK UL01 uń6as uNg°l '
a19 = 'AmPu74 b1l@T b!N|broCh4 B0b° 8ø6o b0t0 bRok#4 8ur@T BµYzIT đ3M0Ny0 3n60T g4gO H@y0P hYNaYUPAK #UđA5 inIyøt inu71l 1y0t ;4col Kag4Guh4N k4Nt0t KagntUT4n caulU1@N cYcE cicYngIgn4mo kiN6Ira KuP4l 1EkhE lYNt|c n4k4k4bur4t O10c paC!gn6Zh3t P4CShET paKYU P0KP0K pUkh4 PUc#An6g4l4 pukhAngY2A Puc3 Puc|µang!Na PUnY374 pU74 Pu74n6InA PUt@RagYS Ra7bu zhunga s|r4u10 SuSo T@E T@eµ4 T4m0Ð 74ñgA 74NgIn4 taR46IS 7aRANtaÐ0 7imAń6 tiT3 TUNg4W ugOK UL01 uń6as uNg°l'
a20 = '4mPU74 8|l47 81ńYbR0c#@ 8*80 8060 80t0 bR0kh4 8Ur4t bW15Y7 D3M06ny* 3µG07 6460 #4y0P #Yµ4Yup4k Huđ4S |ńyY*7 1gnU7|1 1y07 ;4c0l k46@6Uh4ń c46grt0t c46ń7uT4g6N k@U1u14ń kYk3 C|c1µ6|ñAM* CYµ6Yń4 kup41 l3k4E 1!ń7!c N4C4k@8ur47 0L0k P4C1µg5h37 p4c5#3t p@cyu P0kP0c Puk#4 pUc4@ñ66@14 Puk4@gµ61ń4 puk3 pUc1#4µg!ńa PUny374 pu74 Pu7@n6|6Gµ4 PU7@R4g|5 r47bU 54UgµG@ S|r4Ul* 5Uz0 7@3 743n@ 7@MøD t4µ64 t@N6!ñ@ 74r@6Y5 7@r@gGnT4Ð0 7!M4µ6 ty7e 7uGn64w U60c Ul01 un645 Uñ601'
a21 = '4mpU74 8|l47 81myBR0ch@ 8()80 8060 80t0 8r0KH4 8UR4T 8w15y7 d3m06ny00 3ng()7 6460 h4Y00P hYñ4yUp4C hud4z |ńyY()7 1nu7|1 1Y07 ;4c0l K46@6Uh4gn C466nT0T k46ñ7UT4g@n c@u1u14ñ cyK3 K|c1n6|n@m0 cYn6yñ4 cuP41 13c]-[3 1!ñ7!C n4C4c@8Ur47 0lOk P4K1N65]-[37 P4c5h3T P@cYU p0kP0k pUCh* pvCh@n66@14 pUCh@gñ6!n4 pUc3 Puc1n4ñG!na Pugny3T4 pu74 PU7@gn6|6gñ4 Pu7@R4gY5 R4tBu 5]-[uGnG@ s|R4ul() 5UZ0 7@3 t43n@ 7@m()d 74n64 7@n6!n@ 74r@6!5 7@rag6nT4D0 7!m4n! tî73 7ugN64W U60c ul01 UN64S vN601'
a22 = '4mpu74 8|l47 b1ńYbr0Ch@ 8ô80 8060 8070 8r0Ch4 8uR4t bW15Y7 D3m06nYo 3ng07 6460 hh4Y0P hyn4YUp4k hu|)4s |n!y()7 1nu7|1 1y07 ;4k0l K46@6uh46n k46gñT0t c46n7U746gn k@u1U14n cyC3 c|k1ń6|namm0 cin6yñ4 cvP41 L3chE 1!n7!C gn4c4C@8UR47 010k p4k1gnG5H37 P4c5h37 p@CYU P0cP0c fvKh4 pUkh@n66@14 Puch@Gh6ih4 PUc3 pUC1]\[@ng!ña PUNY374 PU74 pU7@n6|66ń4 PU7@R46I5 R4TbU 5huGn6@ Z|R4UL() 5U50 7@3 T43n@ 7@m()d T4]\[64 7@n6!nn@ 74r@6|5 7@R4gGnt4d0 7!m4n6 tY73 7UgN64ww U60k u101 Uń645 Uñ601'
a23 = '@mpuT4 8|147 b1ñYbr0ch@ 8*80 8060 b0T0 8R0C#4 8UR4t 8W15|7 D3M06nY0 3ñg07 g@60 #4y0p 4Y24yUp4C huÐ4z |Nyy*7 1ñU7|1 iY07 ;4c0l K4g46Uh4Gñ k4gNT0t k46ñ7uT4ggn k@U1U14n cyK3 C|K1µg|ñAM* kYµGyñ4 cUP41 l3cHe Liµ7!K nAC4K@8uR47 010c PaK1ng5h37 p4K5#37 p@cyU p0kP0C puc#4 PUC4@µ66@14 PuchagN6iµ4 Puk3 Puc1ñaµg!µ4 punY374 pu74 pu7@n6|6gn4 puT@r4G!5 R478u 5#UgnG@ 5|r4ulO 5uz0 7@3 T@3n4 7@M*Ð 74ñ64 7@N6µ!@ t4R@6!5 7@R4gnt4d0 7!MAñ6 7y7E 7uñ64w u60k U10l uñG45 uµg01'
a24 = '4mPU74 8|1a7 b1µYBR0ch@ 8*80 8060 b0t0 Br0KH4 8UR4t bw15i7 d3M06Ny0 3µG07 6460 #4y0p 4yñ4yUPAC huÐ4s |]\[yY()7 1nU7|1 !Y07 ;4kO1 C4G46uH4G]\[ c46|\|T0t cAGn7uTaggn c@U1U14|\| kyC3 k|K1]\[g||\|A]\/[() cY|\|Gy|\|4 cUP41 lEc]-[3 1Y]\[7!c nak4k@8uR47 o10c p@C1|\|g5h37 P4c5]-[3T p@CYu P0kP0k pUc]-[4 pUC]-[@]\[66@14 puCh4g]\[6i]\[4 puk3 PUC1]\[4|\|G!]\[A PUnY374 pU74 pUT@n6|6gN4 pUt@r4615 R478U 5]-[uGNg@ Z|r4uL0 5UZ0 7@3 tA3|\|4 7@]\/[()d t4]\[64 T@n6!]\[@ t4r@6!5 7@rag|\|T4d0 7!]\/[4]\[6 TY73 7Ugn64\/\/ u60k ul0L ung4s u]\[g01'
a25 = '4MPuT4 8|La7 b1|\|YbR0C]-[@ 8()80 8060 b0t0 Br0CHA 8ur4T Bw15!7 D3]\/[06Ny0 3|\|g07 gA60 ]-[4Y0p ]-[Y|\|4yup@C Hu|)4S |]\[YY()7 1]\[u7|1 iY07 ;4k0l C4Ga6UH46]\[ c46nTot k4Gn7uTagGn C@U1u14n kYK3 K|k1]\[6||\|a]\/[() cy|\|Gy|\|4 kUP41 l3ch3 L1]\[7!C n4c4k@8uR4T ol()c Pak1ng5H37 p4k5]-[3T P@cYU P0CpOk pUC]-[4 PUc]-[@]\[66@14 PUCh4Gn6|]\[4 PUc3 PUk1]\[a|\|G!]\[@ PunY3t4 pU74 Pu7@|\|6|6Gn4 Pu7@r46!5 r47BU 5]-[ugnG@ S|R4ul0 5uz0 7@3 743nA 7@]\/[()d T4]\[64 t@n6!]\[@ t4R@6iZ 7@Ra6Nt4|)0 7!]\/[A]\[6 TY7E 7un64W U60k ul0L ung4s u]\[g01 '
a26 = '@MPU74 8|L47 B1|\|Y8R0cH@ 8()80 8060 B070 BR0cHA 8UR4T Bw15i7 d3]\/[06nyO 3|\|g07 g@60 ]-[4y0p ]-[Y|\|4YUP4C hu|)4s |]\[yY()7 1gnu7|1 YY07 ;4kol C4g46UH4gN k4gNT()7 CA6n7uTa6ggn c@u1u14n KyK3 C|k1]\[G||\|@]\/[() KY|\|gy|\|4 kUp41 l3chE l|]\[7!C n4C4K@8uR4t ol()c P4K1ng5H37 p4C5]-[3t P@CYu p0kpok PuK]-[4 pUc]-[@]\[66@14 pUk]-[4G|\|6|]\[4 Puc3 Puk1]\[A|\|G!]\[a PUny374 pU74 PuT@N6|6Gn4 PuT@R4GY5 r4TBu 5]-[ug]\[g@ S|R4U1() 5u50 7@3 743gn4 7@]\/[()d T4]\[64 7@N6!]\[@ 74R@6|Z 7@r46gnT4|)0 7!]\/[4]\[6 tY73 7un64w u60c UL0l uN645 u]\[g01'
a27 = '4MPUT4 8|la7 B1ñYbr0c]-[@ 8()b0 8060 BO70 Br0kh4 BUr47 bw1z!T d3]\/[0GnyO 3ɲGo7 g460 h4Y0p HInaYuPac huD4S YnYyo7 Ynu7|1 IY07 ;4c0l c4g46Uh4ggn K4gn7OT kag|\|TU74gn K4u1u14n cyk3 kiCi]\[g||\|4]\/[() CY|\|6Y|\|4 cup41 lechE Li]\[t!k ]\[@k4C@bUR4t 0l()C paC1ng5]-[3T P4C5]-[3t p@cYU P0cP()c puk]-[4 pUc]-[A]\[G6@l4 PUCH@n6|]\[4 PuKE pUc1]\[4|\|G!]\[A PUnY374 PU74 pU7@]\[6ig|\|a pu7@r4gi5 R47bu 5]-[u]\[GA 5|r4Ul0 5uS0 t@3 7a3na t@]\/[()D t4]\[g4 T4]\[6!]\[@ 74R@6Ys 7@Ra6]\[t4d0 t!]\/[an6 7Y73 7Un64W U60k U10l UN64z UNgo1'
a28 = '4mpUT4 b|l47 b1ńYbr()C]-[@ 8()80 8060 8OT0 br0kha 8urAt Bw15iT D3]\/[0gNY() 3ɳgO7 GA60 ]-[4y0p ]-[!ṋayupaC HUd4Z inYYO7 |nU7|1 iY07 ;4kOl k4646uh4g]\[ k4g|\|tot kagnTu7Aggn cAu1U14N kyc3 cIC|]\[G1|\|@]\/[() ky|\|6Y|\|4 cUp41 LEKh3 1!]\[t!C n4c4k@BUr47 Ol0C P4c1ng5HeT P4c5]-[37 p@cYU p0KP0k puk]-[4 Puc]-[a]\[66@l4 pUkh4gn6|]\[4 Puc3 PuC1n@|\|6!]\[a PUNY3T4 pUt4 PU7@n6YgN4 pU7@R46|5 R478U 5]-[unGA 5|R4ulO 5uz0 t@3 t43na t@]\/[0d T4NG4 7@n6!]\[@ 74r@6YS 7@ra6gnT4DO T!]\/[4n6 tYt3 7u]\[64\/\/ U60k U10l Ung4z UNgo1'
a29 = '4mPUt4 B|la7 b1nybR0ch@ 8ôB0 8060 BôT0 bR0Ch4 Bura7 8w15!7 d3m0GnYô 3NGO7 6A60 h4Y0p hYn4yuP4K hud4s |nyYo7 !Nu7|1 Yy07 ;4cO1 k@g46uh46N K46N7Ot caGn7U7@Gn c4U1ul4n cYC3 C1kYn6!naMô Kyñ6Yñ4 kUp41 l3k#3 l1ñt!C ñ4c4c@BUR47 Ol0C pAc1nG5He7 P4K5h3T P@kyu p0cpok PuC#4 pUc#@ñG6@l4 PucH4N6Iñ4 pUc3 pUc1NAńg!ń4 pUNy3T4 Put4 PUt@n6|6N@ put@R4g15 RaTbu 5#unG@ Z|R4UL0 5US0 T@3 Ta3n@ T@M0d t4nG4 TAN6!ń@ T4r@6!s 7@ra6ńt4d0 t!M4N6 TY73 7Uń64w U60c u101 UNg4z Ungo1'
a30 = 'ampU74 b|La7 b1ñybR0ch@ bøb0 8060 80T0 8R0cḣ@ 8uRaT 8W1Sit d3ṁ0gNyö 3#g07 6a60 h4y0p H!gn4Yupac Hud4z |Nyy07 1ɲu7|1 1y07 ;4k0l c@g46uh4gN k4ggnt07 C@gN7U74gɲ cAu1Ul4N cYK3 cic1ɲgIŋaMô kYNgYñ4 CUp41 lEcHE LIń7!c Nak4k@Bur47 0Lok p4k1gng5#37 p4K5#3T p@CyU P0Cpok PUk#4 PUC#AṅG6@14 pUkhAN6Yṅ4 Puce puc1N4ṅg!ṅ4 PugnY3t4 pu74 PUT@n6IgN@ pU7@r4g15 rA7BU 5ḣun64 s|r4u1o 5uZ0 T@3 t43N@ t@ḿod T4gng4 t@n6!ņ@ t4r@6!S 7@Ra6n74d0 t!ᵯ@N6 Ty73 7Ugn64w U6oc UL01 UNg4s ugnG01'
b6 = 'atupma talib ahcorbinib obob ogob otob ahcorb tarub tisiwb oynomed togne ogag poyah kapuyanih saduh toyini lituni toyi lokaj nahugagak totnak natutnak naluluak ekik omanignikik anignik lapuk ehcel kitnil tarubakakan kolo tehsgnikap tehskap uykap kopkop ahcup alaggnahcup anignahcup ekup anignanikup ateynup atup anignatup sigaratup ubtar agnuhs oluaris osus eat aneat domat agnat anignat sigarat odatnarat gnamit etit wagnut kogu lolu sagnu lognu'
b1 = 'amputi bilhan borachio baba goblin boot branch karat bawas damhin bingot ago halip halimuyak hugas iniyak gentil iyo jaryo kalihiman kanton kanluran kailaliman kiko kikilananin kalamnan kapal little intsik nakakabuhat kaloy paking pakainet kalbo pakpak punch puspusan pitongput laki kanikanina panata pata pintuan paramabilis rabies siomai sarao piso tea talong tanglad panga tanglad galis latrant tamang tito langaw ugat ukol sungay gulo' 
b2 = 'armpit buhat bronchia bibo bago bayot broca buhat buwis damayo eliot gado halik halimaw ubas sinibak inutal kyot dyaryo kaligayahan karton kantunan kauluhan kako kakilala kanina tagal litter antik nakakabilib kilo pakikishot palakpak kalbu palakpak planet pichapie pulangtupa paki kanina punet bata pinamana pagtanggal ratrat siopao sirangplaka paso tali tinola tulog banga talangka tatagos tarlatan palamang siko lugaw sugat bukol singa galing'
b3 = 'mabuti bigat broncho bob logo abot boka buhay bwaya money eight cargo haplos alitaptap malas inyo nautal tuyot jake kagandahan karmot kwentuhan kailangan peke kalakasan kilabot kalkal lechon linta nakikibahay lolo pekengshot pakita labyu tuktok purse pulanggala pitongtupa pake prutasan pinya tapa pamana pagtanggol butas tinga sarado puso trio tanaw tanod tatlo tinapay tiniklop tomato lima lite uhaw higop iloilo anus unggoy'
b4 = 'maputi silat binarios dodo globo vote bench bulsa bulag domain lungkot grado hanay hintuturo butas binagyo until isda jargon kalungkutan kentucky panotcha kikiam kiskisan hilaga kalamnan tapal leyte chinese buraot tulog arcaneshot tape taho tugtog pula dahon pusa poke poking pustahan prutas pamintuan tiniris tirik simple aris choco tao relo daloy hikaw ngiti gisado tarantula timog lilac tanaw bulok untog ingat gulong'
b5 = 'angtupa sikat boracay vivo bygon tungo bleach bahay bureau demolition lagot hotdog hayahay hinlalaki hugasan haiti iowa sayo jackenpoy kangaroo natakot centaur callalily cycle madamo queen lapagam letson checking nakakabagot alias pinocchio peccan pakulay tiktok bacha balangga punching lake pamangkin peanut pasa antigun guitar bukal tsina sierra buko kalye pahina atom bangka makina teargas tartana semplang bati tanglaw tagak ulap hugas bungal'


dictionary = dict.fromkeys(raw_profanity,{})
dictionary2 = dict.fromkeys(raw_profanity,{})
fi = first.split(' ')
se = second.split(' ')
th = third.split(' ')
fo = first.split(' ')
fif = fifth.split(' ')
six = sixth.split(' ')
sev = seventh.split(' ')
ei = eight.split(' ')
ni = nineth.split(' ')
ten = tenth.split(' ')
h1 = b1.split(' ')
h2 = b2.split(' ')
h3 = b3.split(' ')
h4 = b4.split(' ')
h5 = b5.split(' ')
h6 = b6.split(' ')
l1 = a11.split(' ')
l2 = a12.split(' ')
l3 = a13.split(' ')
l4 = a14.split(' ')
l5 = a15.split(' ')
l6 = a16.split(' ')
l7 = a17.split(' ')
l8 = a18.split(' ')
l9 = a19.split(' ')
l10 = a20.split(' ')
l11 = a21.split(' ')
l12 = a22.split(' ')
l13 = a23.split(' ')
l14 = a24.split(' ')
l15 = a25.split(' ')
l16 = a26.split(' ')
l17 = a27.split(' ')
l18 = a28.split(' ')
l19 = a29.split(' ')
l20 = a30.split(' ')

xtotal = 0

def clean_value(word):
    threshold = 0.99
    string = to_lowercase(word)
    tokens = whitespace_tokenizer(string)
    tokens = leet_checker(tokens)
    tokens = stopwords_checker(tokens)
    tokens = filipino_word_checker(tokens)
    tokens = init_default_values(tokens)
    # tokens = init_default_values(filipino_word_checker(stopwords_checker((leet_checker(whitespace_tokenizer(string))))))
    for key, value in tokens.items():

        if value['isStopword'] == False and value['isDictionaryWord'] == False:
            if value['isLeet'] == True:
                x = [x for x in raw_profanity if jaro_Winkler(value['originalWord'],x) >= threshold]
                if x:
                    tokens[key]['isProfane']  = True
                else:
                    tokens[key]['isProfane']  = False
            else:
                x = [x for x in raw_profanity if jaro_Winkler(key,x) >= threshold]
                if x:
                    tokens[key]['isProfane']  = True
                else:
                    tokens[key]['isProfane']  = False
        else:
            continue
    for key,value in tokens.items():
        if value['isProfane'] == True:
            return True
        elif value['isProfane'] == False: 
            return False

# print(clean_value('ibon'))
i=0


start = time.time()
for key in dictionary:
    if i != 62:
        dictionary.update(
            { 
                key: 
                    {
                        fi[i]: clean_value(fi[i]),
                        se[i]:clean_value(se[i]),
                        th[i]:clean_value(th[i]),
                        fo[i]:clean_value(fo[i]),
                        fif[i]:clean_value(fif[i]),
                        six[i]:clean_value(six[i]),
                        sev[i]:clean_value(sev[i]),
                        ei[i]:clean_value(ei[i]),
                        ni[i]:clean_value(ni[i]),
                        ten[i]:clean_value(ten[i]),
                        l1[i]:clean_value(l1[i]),
                        l2[i]:clean_value(l2[i]),
                        l3[i]:clean_value(l3[i]),
                        l4[i]:clean_value(l4[i]),
                        l5[i]:clean_value(l5[i]),
                        l6[i]:clean_value(l6[i]),
                        l7[i]:clean_value(l7[i]),
                        l8[i]:clean_value(l8[i]),
                        l9[i]:clean_value(l9[i]),
                        l10[i]:clean_value(l10[i]),
                        l11[i]:clean_value(l11[i]),
                        l12[i]:clean_value(l12[i]),
                        l13[i]:clean_value(l13[i]),
                        l14[i]:clean_value(l14[i]),
                        l15[i]:clean_value(l15[i]),
                        l16[i]:clean_value(l16[i]),
                        l17[i]:clean_value(l17[i]),
                        l18[i]:clean_value(l18[i]),
                        l19[i]:clean_value(l19[i]),
                        l20[i]:clean_value(l20[i]),
                        
                        # h1[i]: clean_value(h1[i]),
                        # h2[i]: clean_value(h2[i]),
                        # h3[i]: clean_value(h3[i]),
                        # h4[i]: clean_value(h4[i]),
                        # h5[i]: clean_value(h5[i]),
                        # h6[i]: clean_value(h6[i]),
                    }
            }
        )
        i+=1
i=0
for key in dictionary2:
    if i != 62:
        dictionary2.update(
            { 
                key: 
                    {
                        h1[i]: clean_value(h1[i]),
                        h2[i]: clean_value(h2[i]),
                        h3[i]: clean_value(h3[i]),
                        h4[i]: clean_value(h4[i]),
                        h5[i]: clean_value(h5[i]),
                        h6[i]: clean_value(h6[i]),
                    }
            }
        )
        i+=1

# print(clean_value('amputa'))

# total number of comparisons(TRUE) =   31*62 = 1922  (86%)
# total number of comparisons(FALSE) =   5*62 = 310   (14%)
# total number of comparisons       =   36*62 = 2232 (100%)
# for key, value in dictionary.items():
#     print(key, value)

# for key, value in dictionary.items():
# xtotal = sum(len(value) for value in dictionary.values())
# ytotal = sum(len(value) for value in dictionary2.values())

tp = 0 # number of instances correctly predictied that belong to the positive class
fp = 0 # number of instances incorrectly predicted that belong to the negative class
fn = 0 # number of instances incorrectly predicted that belong to the positive class
tn = 0 # number of instances correctly predicted that belong to the negative class
for key, value in dictionary.items():
    for value2 in value.values():
        if value2:
            tp+=1
        else:
            fn+=1

for key, value in dictionary2.items():
    for value2 in value.values():
        if not value2:
            tn+=1
        else:
            fp+=1
print('True Positive: ', tp) 
print('False Negative: ', fn)
print('False Positive: ', fp)
print('True Negative: ', tn)

print('Total: ', fn+tp+tn+fp)
# print('Total True Positive: ', xtotal)
# print('Total True Negative: ', ytotal)
end = time.time()
print('time: ', end - start)

# dictionary = 1,511
# dictionary2 = 371 

    
