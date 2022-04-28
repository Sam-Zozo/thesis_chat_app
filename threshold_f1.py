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

first = '4mPut4 b!L4T b!N1br()kh@ bObO 806o bo70 Br0cha BurAt 8\/\/1SI7 d3m()nY() 3ng0T g46() ]-[4yOP HinaYUp4c ]-[Udas 1n!Y0T |nUtil iYO7 jac()L CaG4guH4n k4n70T K4NtUt4|\| c4ululAn cYke c!k!Ng1n@mO cYgnGY|\|A kUPAl l3c]-[3 l1NTik gnaK4cAbura7 0LoK paKYnG5h3T Pakzh37 p4cyU P0Cp0C pUCha PuChA]\[G64la pUchAgnGIna puC3 PUkin4gnG|n4 puNY3ta PUTa puTangiNA pUt4ragiZ raT8U SHUnGa s1R4ul() 5U50 T43 ta3]\[4 t4m0|) 74gnG4 t4nGiN4 t4R46|z taR4n7@|)o 7!]\/[@ng 7|t3 7uNGaw Ug()K ulOL unG4s ugn60L'
second = 'ampUT4 bil4t binibr0ch4 b0b0 b0g0 b0t0 br0ch4 bur4t bwisit d3m0ny0 3ng0t g4g0 h4y0p hin4yup4k hud4z iniy0t inutil iy0t j4k0l k4g4guh4n k4nt0t k4ntut4n k4ulul4n kik3 kikingin4m0 kingin4 kup4l l3ch3 lintik n4k4k4bur4t 0l0k p4kingsh3t p4ksh3t p4kyu p0kp0k puch4 puch4ngg4l4 puch4ngin4 puk3 pukin4ngin4 puny3t4 put4 put4ngin4 put4r4giz r4tbu shung4 sir4ul0 sus0 t43 t43n4 t4m0d t4ng4 t4ngin4 t4r4giz t4r4nt4d0 tid00dg tit3 tung4w ug0k ululz ung4z ung0l'
third = '@mpuT4 b|1aT B||\|!Br()c]-[4 bOb() b()6() 8()T() BrOch4 Bur4T bWYsYT D3]\/[0ny0 ENG0T 6AG0 hay0P hYN@yup4k hUD@z 1]\[|Y07 ||\|u7|l |y07 ;AKo1 C@G46U]-[Agn CANT0T k4n7uT4gn caUlu1AN C1cE kiCY|\|gYn@m0 cY|\|g1|\|a cup@l l3Ch3 l1n7|k nAC4KaBurat 0l0C p4K1NgZHet p@KshEt pakYu PocP0K Puk]-[4 PUkh@Ngg@L4 PUk]-[4]\[GIna PUC3 pucIgn4nGYnA Punye74 puta pUT4N6ign4 PU7aRag!S ratbU ShunGa zIraUl0 Su50 Ta3 T43n4 7@M0d 74gnga t4nGin@ 7@rAgYs 7Ar4gnT4|)() TimaN6 TY7e TUng@w u60k Ul0l unGa5 ung0L'
forth = '@4mpU7a B11@T 8INIBr()ChA 80b() B0g() b0t0 BrOc]-[A Burat bWizit Dem()Ny0 3nGot gAgo hay0P H1|\|4yuPAC Hud@z 1]\[iY07 InU7Y1 |y07 ;acol kAGaGuh4n k4nt07 K4]\[tut4n c4ulu1An kYke kIKYgngi]\[amO CYNGIgn4 KUpAl LEC]-[3 L|]\[t|c nak@k4bur4t 0l0k pakInGZH3T PaCSh3t PAcYu P()CP()C pukhA PUc]-[4ngG414 puCh@nGinA PuCe PucYnangIn4 Pu|\|y3ta PutA Putan6I|\|a Put4R@g!z Ra7bU sHun64 Z|RauL0 ZU5O 7@3 Ta3nA T4M0d 7@Nga 74|\|gin@ TaR4GY5 TAr4n7@|)() 71M4Ng 7i7E 7uNg@w uG0C Ul()L uNGAS unG01'
fifth = '4MPU74 b!147 binYbR()cH@ b0bO b0g() b()t() BRokh4 buRat BW!z|7 d3monY() eN6()7 g4G0 h@Y0P ]-[!|\|@yUp4K ]-[UDas ign|yot !gnUt11 |y0t ;aC0l K4g4gu]-[4]\[ c4|\|tOT K@gnTuTAn C4UluL4]\[ k|Ce c!cin6iNAm0 KYngYN4 KuP41 LEk]-[E l1N7iK NaKakABURAT o10c p4C!ngzH3T PacSh3T p4KYU P0cP()c PuCha pukHAn6GAl4 pUk]-[4gngYgn@ pUK3 Pukin4ngI]\[4 pugnYEtA pUTa Pu7agngYgnA PU74R4g1z r4tBU SHUnGA Z|r4Ul0 suso tA3 Ta3na 7Am()D 7@Ng4 T4]\[GY|\|4 taR46Ys t@r4ntad0 t|]\/[4n6 7It3 tUn64\/\/ Ug()C Ulo1 U|\|G4Z UNG()L'
sixth ='4mPuTa 81l4t BYgn!brocH4 8oB0 b()GO B()70 bR0kh4 bUR4T b\/\/iz17 d3]\/[()nyO 3nG07 gaG() H4y()p ]-[||\|4YUp4K ]-[U|)45 1nYy07 1nU7!l !yO7 J4C0l k4gagUHA|\| ka]\[7()7 k4]\[7Utan C4ulu14]\[ k1ce c!c!nGYn@]\/[0 c!Ng1|\|4 cupaL 13kh3 l|n7ic ]\[@KAC@bUR@t O1OK P4CIgnGZ]-[E7 PakS]-[Et paCyu p0CpoC pUc]-[a PUk]-[4nGG4L4 pukh4|\|6|na pUce PuKi]\[4nGYn4 PUnyE7@ PU74 PuT4ngIn4 PUtaR4615 rAtBU zHU]\[6a zIR4ulo 5U5o 7Ae T43|\|A t@mo|) 7@NGa 7A|\|g|]\[a T4r4g!Z taR4|\|t4D0 Tim4Ng TI73 7un64w u60K Ul0l un64z un60l'
seventh = '@Mpu7@ b!14t B!gnIbR0kHa BOb() Bog() 8Oto br0kh4 buR4t bW151t |)3m()ny0 Egng0T g4g() h4yOP ]-[|n4YuP4k HUDAz YN!y0T i]\[Ut!L |yoT ;@Kol k4g@guh4]\[ CanT0t canTutaN KaU1Ul4gn C1Ce c!kIgnGYnAm0 cYn61N@ cUPAL 13kh3 LYNt|c ]\[aKak48URat ()10k P4K||\|gZH37 P4kSHe7 pacyU p0kpOC pUkh4 pukH4Ngg41a pUkhAng1n4 pUc3 pUCi|\|4|\|G|gn4 PUnyEta PUT4 PU7@|\|6!Na PUt@Ra6Ys ratbU 5hU|\|64 S!r4U10 5us0 T43 7aENA Tamo|) t4|\|G4 T4|\|6|n4 T4r4Gis 7aR4nT@Do 7!]\/[4gn6 TIt3 tu]\[6a\/\/ U6Ok Ul0l Un6Az uNg0L'
eight = 'AMpuTa b!14t B!gnIbR0kHa BOb() Bog() 8Oto br0kh4 buR4t bW151t |)3m()ny0 Egng0T g4g() h4yOP ]-[|n4YuP4k HUDAz YN!y0T i]\[Ut!L |yoT ;@Kol k4g@guh4]\[ CanT0t canTutaN KaU1Ul4gn C1Ce c!kIgnGYnAm0 cYn61N@ cUPAL 13kh3 LYNt|c ]\[aKak48URat ()10k P4K||\|gZH37 P4kSHe7 pacyU p0kpOC pUkh4 pukH4Ngg41a pUkhAng1n4 pUc3 pUCi|\|4|\|G|gn4 PUnyEta PUT4 PU7@|\|6!Na PUt@Ra6Ys ratbU 5hU|\|64 S!r4U10 5us0 T43 7aENA Tamo|) t4|\|G4 T4|\|6|n4 T4r4Gis 7aR4nT@Do 7!]\/[4gn6 TIt3 tu]\[6a\/\/ U6Ok Ul0l Un6Az uNg0L'
# nineth ='4mpuT4 8|1@t b!Nibr0ch4 b()b0 bOg0 b0t() 8r()kH4 bur47 bWis|t D3m0gnY0 3Ng07 G@6o ]-[Ay0p hYn4YuPaK hU|)@s InYY0t !nu7Yl iyoT jAK01 C4gagUH@N C4N7()T ca|\|tut4n cAuLUl4n kikE cik1|\|6InA]\/[() k!nGina cupal 13k]-[e LYn7!C |\|4Cak4buR@7 0l()C p4k1n6sH3t PAKShEt pacyu p0cpOc pUCh4 pukH4ng64l4 PuChang1na PuKE pUkIgn@nG!|\|A punyE74 Put4 Pu74n6!N4 putaR4gi5 RA7Bu ZHugnGa sIR4uL0 zusO T@E T43n4 TaM0d 7AN64 Ta]\[GiNa 7ar4GIS t4r4gnT4|)0 7ima]\[6 tit3 7Unga\/\/ ug0C u1ol u]\[gAz UnGOl'
nineth = '@MpuTA bYla7 bY|\|YbRoKha 8O8() b060 80t0 8R()C]-[4 bur@t 8W|sYT dEm0ny() 3|\|g0t g460 H@Y0P hY|\|@yuP4K hU|)4S I|\|1Y0T !|\|U7yl IY()t ;4k01 k@g4GUh4n c4nT()T C@]\[7uta]\[ c4u1U14]\[ cYc3 k1k|gn6Ygn4]\/[0 C!ng1gn4 kUP41 1Ek]-[e 1|Nt1K |\|AC@c4bUR@7 0loc P4cy]\[g5h37 p4kZ]-[37 PAkyU p0kP0k puCH4 pUc]-[AnG64L4 pukh4gng!gn@ Puk3 puk1|\|@]\[61gna PU|\|Y3t4 pUt4 pUT@gn6!NA pu74R@6y5 R47bu Zhu|\|g4 zYr4uL0 ZuZ() t43 T43GgnA 74]\/[0|) 74GNG4 t@g]\[Gy|\|a 74rag1S 74Ra|\|T4d0 t!m4]\[6 T|7e 7u]\[G4w uG0k UL01 Ung45 U|\|601'
tenth = 'AMpU74 8Y1aT b!nYBROkH4 bOb0 B()6o BOT0 bRokhA buRa7 bWYzit |)3]\/[oNyO enG07 ga60 h4y()p ]-[1NAYUP4k HU|)AS IniY()T i]\[UtIl iy0T ;@ko1 k4g46Uh4N kaNt0t c4ntUt@n C4UluLAgn CIcE CIk1n6I|\|4mO k||\|g1]\[@ kUPaL L3kh3 1|]\[7ic |\|aCak@8uRat OL0c PAKi|\|gzh3t p4CShe7 P4kYU p()cP0k pukH4 pUCh4nGG4L4 pUChaNgINA PuKE PuCIgn@nG1]\[4 PUnYe7a Put4 puTagng!gn4 pUT@R@6YS raTBu zhunga S|r4Ulo suzO T43 ta3n4 ta]\/[0D tanGa t4ngin4 TAr@GYZ T4rAgn7@dO T!M4ng tit3 7ugnGaw UG0c ULo1 UNg4S ugn6OL'
a11 = 'ampU7a bil@7 b1]\[!br()Cha b0b() 80G0 b()70 br()kH@ 8Ura7 B\/\/iS|T dEm()nyO eNg0t g46() ]-[@Y0P hYn4YuPaK hUd4Z |]\[|Y()t YnU7Y1 |Y07 ;aK()1 c4g4guh@n caNT()7 cA|\|7uT@n C4ulULAN KYC3 c|C|ngIna]\/[() C!ng!gn4 cuP@1 lEch3 LiNTYK gn@C@cAbUR@7 01()c p4C!Ngsh37 Paczhe7 PakYu P()KP0c PUch@ PUkh4ngg4La pUkh4Ng1|\|a PUC3 PUC1n4]\[6|na PUNYE7@ PuT4 PU74gng!N@ PuT4R46is R4T8U 5Hu]\[G4 5iR4U1O sUs() t@3 ta3na 7AmOd tagnga ta|\|6!Na T4r4g|5 t4r@nt4D0 71m4nG 71t3 7un64w ug()k ul01 UnGaz Un60L'
a12 = 'AmpU7@ b1l@t b!NY8r0Ch@ Bobo B0go B0t0 bRok]-[@ bURa7 b\/\/!Zit d3M0ny() e|\|60T gag0 ]-[@Y0p HiN4yUpAk ]-[u|)aS !]\[|y0T i]\[u7Y1 |Y07 j4K()1 K46@gUh4N k4nT07 canTuT4n K@ulul4N c!K3 kikIN6|NAm0 C!nG!N4 cUpal l3CH3 L!NtIk |\|4k4KabURat 0lok paK|Ng5h37 P4cShET p4kYU P0cP0C PuCha PUc]-[@nGg4la pukHaNgI|\|4 PukE Puk|n@|\|G1|\|a PuNY3T4 Put4 pUTaNgINa PUt4R@GIS Ra7bU zhUng@ s1r4Ulo ZuZ0 ta3 743n4 7aM0D TAng@ TangIN4 taR@6|s t4r4nT4|)0 T|]\/[@Ng TI73 7Ung4w Ug()C uL()L UngaZ Ung0L'
a13 = '4mpu7@ b|LA7 BIni8R0ch@ bOB0 b0g0 bo7() bR()kha buR@7 8wIz1t deM0]\[yo 3|\|goT GaG0 h4Y0p ]-[Y]\[4YUpaC hu|)a5 INYYO7 1NUT1L |YOT jaCo1 ca646u]-[4gn cAN70t C4n7Ut4N c4uLuLAN c|Ke C|cYn6!N4m() c1ngYN4 CUPa1 lekH3 liN7Yc nacACaBuR@7 ()l0k P@K1NgSH3T pAcShET p4cYu p0Cp()k pUC]-[4 PUCh@N66@1A pukhA]\[GY|\|4 pUK3 pUKYgna|\|gin4 pugnY37A puTa puT4ngYN4 put4R@gYZ R4TbU SHUng4 5!r4ul0 sU50 t43 tA3na Ta]\/[od T4N6a T4n6!n4 tArAgIz 7@R4|\|TadO TimanG TIt3 7un6@\/\/ u6()k uL01 uNG4s u]\[601'
a14 = '@mPU74 b1l4T b!]\[YBRokH@ B0B0 80g() B07() bRocHa 8Ura7 8\/\/i5YT d3M0nYo 3ng0T 64g() ]-[4YoP h!gnAYupac ]-[Ud4z INiYO7 Y]\[UTiL iY07 JaKO1 Ka6agUh4N kanT07 k4ntut@n kAuLuLAN kic3 kIC|NG!Na]\/[() ci|\|G!n4 CuPAL l3k]-[3 1!nt|C nac@K48urat 0L()K pAki|\|gzHe7 p@KZhEt P4CYu PokPoK PuCha PUChangg4La pUch4NGi]\[A PUcE pUc|gn4n6iNA PUNY37a pUt@ pUtanGIna puTaR4G!z R4t8U 5hUNGA SIr4ulo zUZ0 ta3 t43na tam0d t@ngA 7a|\|GI]\[a tarAgIz taRanT4|)0 T!m4ng T|te tUnG4W uGoK ul0l Ung4z U|\|g0l'
a15 = 'amPUT@ b!147 BinY8R()kH4 bO80 8OG0 b070 br()kh4 bUR4T bw1S|T |)3M0Ny0 En6o7 g4g0 h4YoP hI|\|ayUP4k hu|)4S !|\|YY0t 1gnu7i1 1yoT j4C0L ka6aguH@gn c4NT07 c4gntuTA]\[ c4ULuL4n CYc3 CYc|n6iN4mO kIn6!NA CuPAL l3C]-[3 l!nT|k gnAk4C@bURaT 0L0k p4k||\|gshEt P4cSH3t P@cyU P0KP0K puc]-[4 Puc]-[4nG6ala PUk]-[Agng!n4 PUce pUKYNAng!]\[A pugny3T@ pu74 PUT4nG!|\|@ PU74RaGYZ R47BU ShUnga zYrAuL0 5uso 743 743gna tAm0|) T@nga ta]\[G1gn4 taraG|Z 7ARant@|)O 7|]\/[aNG 7|te tUn64w U6()c Ul0L uNG45 ungo1'
a16 = '@mpU7a b1l4T b|N1Br0kh4 b0b0 b0GO b070 8roCha bUR4T B\/\/Y5YT d3M0gnYO En6oT g4go h4yoP hiNayupAk ]-[UD@Z INIy()t 1nU7Y1 Yy0T j4c0l ca6A6U]-[an c4NT()t C4]\[7U74N k@ulUL4n KiC3 CIkYnGinaMo cYngiN@ kuPA1 L3CH3 LYnT1C n4c4k4bUr4t ()l()K P4cigngZh37 pAk5HEt pacyU poCp0k PUkHA Puch4ngG4L@ PUch4nG!]\[4 PukE pUk|n4n6Yna PUgny3Ta Pu7a PUTa|\|G|Na PutaragIZ r4TBU S]-[Un6a s!r4uL0 zus0 743 TAena T@mOd 7aNG4 7aNgi|\|4 tar4gI5 t4r4|\|TAd() t|M4nG 7!73 7unGAW uGoc Ul0L unGaZ ugng()l'
a17 = '4mput4 b1lat B||\||bR0c]-[a Bob() bogO boto Br()C]-[a 8Ur47 8w|zIT d3mOgnyo 3nGo7 6ag0 h@Y0p ]-[InayuPak hu|)aS 1n!y0T !nuTIL iy0t j4kOl kagAguh4|\| c4|\|707 C4n7utan C4u1Ulan C!Ce c|K1|\|G1N4M0 CINgIgn4 Kup@1 L3ch3 L!nTIC nacac4buR4T oLOK pAC!ngSh3t P4ks]-[et P@CYU p0KP0k puCh4 Puc]-[anG6a1a PukHa]\[g!n@ PuC3 puK|]\[@n6I]\[a PU|\|YetA puta pUT4nG!n4 PUTaRAgY5 R478u 5hun64 ZIRau1O 5UsO 7Ae 743NA t@]\/[O|) TAng4 7aN6YN@ tar4g!s t4RaNt@d0 t1Ma|\|g 7|t3 Tu]\[g4w UG0k ul0L Ung4Z u]\[g()1'
a18 = 'AmPu74 b1l@T b!N|broCh4 B0b() 8()6o b0t0 bRok]-[4 8ur@T B\/\/YzIT |)3M0Ny0 3n60T g4gO H@y0P hYNaYUPAK ]-[U|)A5 inIy()t inu71l 1y0t ;4col Kag4Guh4N k4Nt0t KagntUT4n caulU1@N cYcE cicYngIgn4mo kiN6I]\[a KuP4l 1EkhE lYNt|c n4k4k4bur4t O10c paC!gn6Zh3t P4CShET paKYU P0KP0K pUkh4 PUc]-[An6g4l4 pukhAngY]\[A Puc3 Puc|]\[ang!Na PUnY374 pU74 Pu74n6InA PUt@RagYS Ra7bu zhunga s|r4u10 SuSo T@E T@e]\[4 T4m0|) 74|\|gA 74NgIn4 taR46IS 7aRANta|)0 7imA|\|6 tiT3 TUNg4W ugOK UL01 u|\|6as uNg()l '
a19 = 'AmPu74 b1l@T b!N|broCh4 B0b() 8()6o b0t0 bRok]-[4 8ur@T B\/\/YzIT |)3M0Ny0 3n60T g4gO H@y0P hYNaYUPAK ]-[U|)A5 inIy()t inu71l 1y0t ;4col Kag4Guh4N k4Nt0t KagntUT4n caulU1@N cYcE cicYngIgn4mo kiN6I]\[a KuP4l 1EkhE lYNt|c n4k4k4bur4t O10c paC!gn6Zh3t P4CShET paKYU P0KP0K pUkh4 PUc]-[An6g4l4 pukhAngY]\[A Puc3 Puc|]\[ang!Na PUnY374 pU74 Pu74n6InA PUt@RagYS Ra7bu zhunga s|r4u10 SuSo T@E T@e]\[4 T4m0|) 74|\|gA 74NgIn4 taR46IS 7aRANta|)0 7imA|\|6 tiT3 TUNg4W ugOK UL01 u|\|6as uNg()l'
a20 = '4mPU74 8|l47 81|\|YbR0c]-[@ 8()80 8060 80t0 bR0kh4 8Ur4t bW15Y7 D3]\/[06ny() 3|\|G07 6460 ]-[4y0P ]-[Y|\|4Yup4k Hu|)4S |]\[yY()7 1gnU7|1 1y07 ;4c0l k46@6Uh4G]\[ c46g]\[t0t c46]\[7uT4g6N k@U1u14|\| kYk3 C|c1]\[6||\|A]\/[() CY|\|6Y|\|4 kup41 l3k]-[E 1!]\[7!c N4C4k@8ur47 0L0k P4C1|\|g5h37 p4c5]-[3t p@cyu P0kP0c Puk]-[4 pUc]-[@]\[66@14 Puk]-[@g]\[61]\[4 puk3 pUc1]\[4|\|g!]\[a PUny374 pu74 Pu7@n6|6G]\[4 PU7@R4g|5 r47bU 5]-[Ug]\[G@ S|r4Ul() 5Uz0 7@3 743n@ 7@]\/[()D t4]\[64 t@N6!]\[@ 74r@6Y5 7@r@gGnT4|)0 7!]\/[4]\[6 ty7e 7uGn64w U60c Ul01 un645 U]\[601'
a21 = '4]\/[pU74 8|l47 81|\|yBR0c]-[@ 8()80 8060 80t0 8r0KH4 8UR4T 8w15y7 d3]\/[06nyO 3|\|g()7 6460 ]-[4Y0P ]-[Y|\|4yUp4C hu|)4S |]\[yY()7 1nu7|1 1Y07 ;4c0l K46@6U]-[4g]\[ C466nT0T k46]\[7UT4ggn c@u1u14|\| cyK3 K|c1]\[6||\|a]\/[() cY|\|6y|\|4 cuP41 13c]-[3 1!]\[7!C n4C4c@8Ur47 0lOk P4K1N65]-[37 P4c5]-[3T P@cYU p0kP0k pUC]-[4 pUC]-[@]\[66@14 pUC]-[@g]\[6Y]\[4 pUc3 Puc1]\[4|\|G!]\[a Pugny3T4 pu74 PU7@gn6|6g]\[4 Pu7@R4gY5 R4tBu 5]-[uGnG@ s|R4ul() 5UZ0 7@3 t43n@ 7@]\/[()d 74]\[64 7@]\[6!]\[@ 74r@6!5 7@rag6nT4D0 7!]\/[4]\[6 tY73 7ugN64W U60c ul01 UN64S U]\[601'
a22 = '4mpu74 8|l47 b1|\|Ybr0C]-[@ 8()80 8060 8070 8r0Ch4 8uR4t bW15Y7 D3]\/[06|\|Yo 3|\|g07 6460 ]-[4Y0P ]-[y|\|4YUp4k hu|)4s |]\[Yy()7 1nu7|1 1y07 ;4k0l K46@6uh46]\[ k46g]\[T0t k46]\[7U746gn k@u1U14|\| cyC3 c|k1]\[6||\|a]\/[() ky|\|6y|\|4 cuP41 L3c]-[E 1!]\[7!C gn4c4C@8UR47 010k p4k1gnG5H37 P4c5]-[37 p@CYU P0cP0c puK]-[4 pUk]-[@]\[66@14 Puc]-[@G]\[6i]\[4 PUc3 pUC1]\[@|\|g!]\[a PUNY374 PU74 pU7@|\|6|66]\[4 PU7@R46I5 R4TbU 5]-[uGn6@ Z|R4UL() 5U50 7@3 T43n@ 7@]\/[()d T4]\[64 7@]\[6!]\[@ 74r@6|5 7@R4gGnt4d0 7!]\/[4]\[6 tY73 7Ug|\|64\/\/ U60k u101 U]\[645 U]\[601'
a23 = '@mpuT4 8|147 b1|\|Ybr0ch@ 8()80 8060 b0T0 8R0C]-[4 8UR4t 8\/\/15|7 D3]\/[06nY0 3|\|g07 g@60 ]-[4y0p ]-[Y|\|4yUp4C hu|)4z |]\[yy()7 1]\[U7|1 iY07 ;4c0l K4g46Uh4G|\| k4gNT0t k46]\[7uT4ggn k@U1U14n cyK3 C|K1]\[g||\|A]\/[() kY|\|Gy|\|4 cUP41 l3cHe Li]\[7!K nAC4K@8uR47 010c PaK1ng5h37 p4K5]-[37 p@cyU p0kP0C puc]-[4 PUC]-[@]\[66@14 PuchagN6i]\[4 Puk3 Puc1]\[a|\|g!]\[4 punY374 pu74 pu7@n6|6gn4 puT@r4G!5 R478u 5]-[UgnG@ 5|r4ulO 5uz0 7@3 T@3n4 7@]\/[()d 74]\[64 7@N6!]\[@ t4R@6!5 7@R4gnt4d0 7!]\/[A]\[6 7y7E 7u|\|64w u60k U10l u|\|G45 u]\[g01'
a24 = '4mPU74 8|1a7 b1|\|YBR0ch@ 8()80 8060 b0t0 Br0KH4 8UR4t bw15i7 d3]\/[06Ny0 3|\|G07 6460 ]-[4y0p ]-[y|\|4yUPAC hu|)4s |]\[yY()7 1nU7|1 !Y07 ;4kO1 C4G46uH4G]\[ c46|\|T0t cAGn7uTaggn c@U1U14|\| kyC3 k|K1]\[g||\|A]\/[() cY|\|Gy|\|4 cUP41 lEc]-[3 1Y]\[7!c nak4k@8uR47 o10c p@C1|\|g5h37 P4c5]-[3T p@CYu P0kP0k pUc]-[4 pUC]-[@]\[66@14 puCh4g]\[6i]\[4 puk3 PUC1]\[4|\|G!]\[A PUnY374 pU74 pUT@n6|6gN4 pUt@r4615 R478U 5]-[uGNg@ Z|r4uL0 5UZ0 7@3 tA3|\|4 7@]\/[()d t4]\[64 T@n6!]\[@ t4r@6!5 7@rag|\|T4d0 7!]\/[4]\[6 TY73 7Ugn64\/\/ u60k ul0L ung4s u]\[g01'
a25 = '4MPuT4 8|La7 b1|\|YbR0C]-[@ 8()80 8060 b0t0 Br0CHA 8ur4T Bw15!7 D3]\/[06Ny0 3|\|g07 gA60 ]-[4Y0p ]-[Y|\|4yup@C Hu|)4S |]\[YY()7 1]\[u7|1 iY07 ;4k0l C4Ga6UH46]\[ c46nTot k4Gn7uTagGn C@U1u14n kYK3 K|k1]\[6||\|a]\/[() cy|\|Gy|\|4 kUP41 l3ch3 L1]\[7!C n4c4k@8uR4T ol()c Pak1ng5H37 p4k5]-[3T P@cYU P0CpOk pUC]-[4 PUc]-[@]\[66@14 PUCh4Gn6|]\[4 PUc3 PUk1]\[a|\|G!]\[@ PunY3t4 pU74 Pu7@|\|6|6Gn4 Pu7@r46!5 r47BU 5]-[ugnG@ S|R4ul0 5uz0 7@3 743nA 7@]\/[()d T4]\[64 t@n6!]\[@ t4R@6iZ 7@Ra6Nt4|)0 7!]\/[A]\[6 TY7E 7un64W U60k ul0L ung4s u]\[g01 '
a26 = '@MPU74 8|L47 B1|\|Y8R0cH@ 8()80 8060 B070 BR0cHA 8UR4T Bw15i7 d3]\/[06nyO 3|\|g07 g@60 ]-[4y0p ]-[Y|\|4YUP4C hu|)4s |]\[yY()7 1gnu7|1 YY07 ;4kol C4g46UH4gN k4gNT()7 CA6n7uTa6ggn c@u1u14n KyK3 C|k1]\[G||\|@]\/[() KY|\|gy|\|4 kUp41 l3chE l|]\[7!C n4C4K@8uR4t ol()c P4K1ng5H37 p4C5]-[3t P@CYu p0kpok PuK]-[4 pUc]-[@]\[66@14 pUk]-[4G|\|6|]\[4 Puc3 Puk1]\[A|\|G!]\[a PUny374 pU74 PuT@N6|6Gn4 PuT@R4GY5 r4TBu 5]-[ug]\[g@ S|R4U1() 5u50 7@3 743gn4 7@]\/[()d T4]\[64 7@N6!]\[@ 74R@6|Z 7@r46gnT4|)0 7!]\/[4]\[6 tY73 7un64w u60c UL0l uN645 u]\[g01'
a27 = '4MPUT4 8|la7 B1|\|Ybr0c]-[@ 8()b0 8060 BO70 Br0kh4 BUr47 bw1z!T d3]\/[0GnyO 3|\|Go7 g460 h4Y0p HInaYuPac huD4S YnYyo7 Ynu7|1 IY07 ;4c0l c4g46Uh4ggn K4gn7OT kag|\|TU74gn K4u1u14n cyk3 kiCi]\[g||\|4]\/[() CY|\|6Y|\|4 cup41 lechE Li]\[t!k ]\[@k4C@bUR4t 0l()C paC1ng5]-[3T P4C5]-[3t p@cYU P0cP()c puk]-[4 pUc]-[A]\[G6@l4 PUCH@n6|]\[4 PuKE pUc1]\[4|\|G!]\[A PUnY374 PU74 pU7@]\[6ig|\|a pu7@r4gi5 R47bu 5]-[u]\[GA 5|r4Ul0 5uS0 t@3 7a3na t@]\/[()D t4]\[g4 T4]\[6!]\[@ 74R@6Ys 7@Ra6]\[t4d0 t!]\/[an6 7Y73 7Un64W U60k U10l UN64z UNgo1'
a28 = '4mpUT4 b|l47 b1|\|Ybr()C]-[@ 8()80 8060 8OT0 br0kha 8urAt B\/\/15iT D3]\/[0gNY() 3|\|gO7 GA60 ]-[4y0p ]-[!]\[ayupaC HUd4Z inYYO7 |nU7|1 iY07 ;4kOl k4646uh4g]\[ k4g|\|tot kagnTu7Aggn cAu1U14N kyc3 cIC|]\[G1|\|@]\/[() ky|\|6Y|\|4 cUp41 LEKh3 1!]\[t!C n4c4k@BUr47 Ol0C P4c1ng5HeT P4c5]-[37 p@cYU p0KP0k puk]-[4 Puc]-[a]\[66@l4 pUkh4gn6|]\[4 Puc3 PuC1n@|\|6!]\[a PUNY3T4 pUt4 PU7@n6YgN4 pU7@R46|5 R478U 5]-[unGA 5|R4ulO 5uz0 t@3 t43na t@]\/[0d T4NG4 7@n6!]\[@ 74r@6YS 7@ra6gnT4DO T!]\/[4n6 tYt3 7u]\[64\/\/ U60k U10l Ung4z UNgo1'
a29 = '4mPUt4 B|la7 b1|\|ybR0c]-[@ 8()B0 8060 B()T0 bR0Ch4 Bura7 8w15!7 d3]\/[0G|\|Y() 3|\|GO7 6A60 h4Y0p hYn4yuP4K hud4s |nyYo7 !Nu7|1 Yy07 ;4cO1 k@g46uh46N K46N7Ot caGn7U7@Gn c4U1ul4]\[ cYC3 C1kY]\[6!|\|a]\/[() Ky|\|6Y|\|4 kUp41 l3k]-[3 l1]\[t!C |\|4c4c@BUR47 Ol0C pAc1nG5He7 P4K5]-[3T P@kyu p0cpok PuC]-[4 pUc]-[@]\[G6@l4 PucH4N6I]\[4 pUc3 pUc1NA|\|g!]\[4 pUNy3T4 Put4 PUt@n6|6N@ put@R4g15 RaTbu 5]-[unG@ Z|R4UL0 5US0 T@3 Ta3n@ T@]\/[0d t4nG4 TAN6!]\[@ T4r@6!s 7@ra6|\|t4d0 t!]\/[4N6 TY73 7U]\[64w U60c u101 UNg4z Ungo1'
a30 = 'ampU74 b|La7 b1|\|ybR0ch@ b()b0 8060 80T0 8R0c]-[@ 8uRaT 8W1Sit d3]\/[0gNy() 3|\|g07 6a60 h4y0p H!gn4Yupac Hud4z |Nyy07 1|\|u7|1 1y07 ;4k0l c@g46uh4gN k4ggnt07 C@gN7U74g|\| cAu1Ul4N cYK3 cic1]\[gI|\|a]\/[() kY|\|gY|\|4 CUp41 lEcHE LI]\[7!c Nak4k@Bur47 0Lok p4k1gng5]-[37 p4K5]-[3T p@CyU P0Cpok PUk]-[4 PUC]-[A]\[G6@14 pUkhAN6Y]\[4 Puce puc1N4|\|g!]\[4 PugnY3t4 pu74 PUT@n6Ig|\|@ pU7@r4g15 rA7BU 5]-[un64 s|r4u1o 5uZ0 T@3 t43N@ t@]\/[od T4gng4 t@n6!]\[@ t4r@6!S 7@Ra6n74d0 t!]\/[@N6 Ty73 7Ugn64\/\/ U6oc UL01 UNg4s ugnG01'
b6 = 'atupma talib ahcorbinib obob ogob otob ahcorb tarub tisiwb oynomed togne ogag poyah kapuyanih saduh toyini lituni toyi lokaj nahugagak totnak natutnak naluluak ekik omanignikik anignik lapuk ehcel kitnil tarubakakan kolo tehsgnikap tehskap uykap kopkop ahcup alaggnahcup anignahcup ekup anignanikup ateynup atup anignatup sigaratup ubtar agnuhs oluaris osus eat aneat domat agnat anignat sigarat odatnarat gnamit etit wagnut kogu lolu sagnu lognu'
b1 = 'amputi bilhan borachio baba goblin boot branch karat bawas damhin bingot ago halip halimuyak hugas iniyak gentil iyo jaryo kalihiman kanton kanluran kailaliman kiko kikilananin kalamnan kapal little intsik nakakabuhat kaloy paking pakainet kalbo pakpak punch puspusan pitongput laki kanikanina panata pata pintuan paramabilis rabies siomai sarao piso tea talong tanglad panga tanglad galis latrant tamang tito langaw ugat ukol sungay gulo' 
b2 = 'armpit buhat bronchia bibo bago bayot broca buhat buwis damayo eliot gado halik halimaw ubas sinibak inutal kyot dyaryo kaligayahan karton kantunan kauluhan kako kakilala kanina tagal litter antik nakakabilib kilo pakikishot palakpak kalbu palakpak planet pichapie pulangtupa paki kanina punet bata pinamana pagtanggal ratrat siopao sirangplaka paso tali tinola tulog banga talangka tatagos tarlatan palamang siko lugaw sugat bukol singa galing'
b3 = 'mabuti bigat broncho bob logo abot boka buhay bwaya money eight cargo haplos alitaptap malas inyo nautal tuyot jake kagandahan karmot kwentuhan kailangan peke kalakasan kilabot kalkal lechon linta nakikibahay lolo pekengshot pakita labyu tuktok purse pulanggala pitongtupa pake prutasan pinya tapa pamana pagtanggol butas tinga sarado puso trio tanaw tanod tatlo tinapay tiniklop tomato lima lite uhaw higop iloilo anus unggoy'
b4 = 'maputi silat binarios dodo globo vote bench bulsa bulag domain lungkot grado hanay hintuturo butas binagyo until isda jargon kalungkutan kentucky panotcha kikiam kiskisan hilaga kalamnan tapal leyte chinese buraot tulog arcaneshot tape taho tugtog pula dahon pusa poke poking pustahan prutas pamintuan tiniris tirik simple aris choco tao relo daloy hikaw ngiti gisado tarantula timog lilac tanaw bulok untog ingat gulong'
b5 = 'angtupa sikat boracay vivo bygon tungo bleach bahay bureau demolition lagot hotdog hayahay hinlalaki hugasan haiti iowa sayo jackenpoy kangaroo natakot centaur callalily cycle madamo queen lapagam letson checking nakakabagot alias pinocchio peccan pakulay tiktok bacha balangga punching lake pamangkin peanut pasa antigun guitar bukal tsina sierra buko kalye pahina atom bangka makina teargas tartana semplang bati tanglaw tagak ulap hugas bungal'


dictionary = dict.fromkeys(raw_profanity,{})
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
        if value['isStopword'] == False:
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

# print(clean_value('amputa'))

# total number of comparisons(TRUE) =   31*62 = 1922  (86%)
# total number of comparisons(FALSE) =   5*62 = 310   (14%)
# total number of comparisons       =   36*62 = 2232 (100%)
# for key, value in dictionary.items():
#     print(key, value)


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
        if not value2:
            tn+=1
        else:
            fp+=1
end = time.time()
print('time: ', end - start)
print('True Negative: ', tn)
print('False Positive: ', fp)
print('True Positive: ', tp)
print('False Negative: ', fn)

# with open('file.txt', 'w') as file:
#     for key, value in dictionary.items():
#         # for value2 in value:
#         file.write('%s:\n\t%s\n' %(key,value))



    
