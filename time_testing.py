import time
from compare import clean_text
from data.raw_profanity import raw_profanity
from jaro_winkler import jaro_Winkler
test_case = [
    [
    "Ang umaga ay maganda",
    "Sobrang init sa tanghali",
    "Sobrang lamig sa gabi",
    "si marcos pala binoto mo kaya ka pala",
    'Leni pala binoto mo kaya ka pala',
    'Ang sakit na may mahal siyang iba',
    'Bakit yung mayaman pa ang pinili niya',
    'Ang sakit lang isipin na wala ka',
    'bagsak na ang pilipinas dahil sa mga botante',
    'Tigil na natin tong relasyon na to',
    ],
    [
    "Ang umaga ay maganda ulul",
    "Sobrang init sa tanghali t@n6in@",
    "Sobrang lamig sa gabi p@kyu",
    "si marcos pala binoto mo kaya ka pala 0b0b",
    'Leni pala binto mo kaya ka pala t@N6@',
    'Ang sakit na may mahal siyang iba taena',
    'Bakit yung tarantado pa ang pinili niya',
    'Ang sakit lang isipin na bobo ka',
    'Babagsak na ang pilipinas dahil sa mga bobotante',
    'Tigil na natin tong relasyon na to t@ng!n@mo',
    ],
    [
    'Ang aga aga puro pang g@g@g0 at k@t@ng4h@n ginagawa mo',
    'Bakit ang taas ng presyo ng gasolina p0t@ng1na @mp0t4',
    'Oo na tama kana t@ng1n4 mo ul0I',
    'hindi ka nakakatuwa panoorin para kang t4n6@ na na uul0l',
    'Ang sarap mabuhay kaso kasama mo ay puro pang g@g4g0 at pang kukup4l',
    'Ang sarap mo pakyu ka para kang gunggong',
    'yung bata umiiyak na dahil sa kabobohan mo putangina mo',
    'tigil tigilan niyo na ang pag ddroga mga hinayupak kayo walang magandang madudulot yan sa inyo mga bobo',
    'ang hindi sumunod sakin bobo at tanga',
    'ang sumunod naman sakin at bobo at tanga padin HAHAHAHA',
    ],
    [
    'ako ay isang b0b0 at siya si t@ng@ at siya naman si t@ng1na',
    'nakaka pvtang!na kayo mga mukhang bvr@t na ulul',
    'bakit ganyan mag isip yang b0b0 hinayupak at t@ng@ na yan',
    'gusto ko lang naman maka punta sa EK pvt@ng!na pakyu ulul kayo',
    'tarantado ang bumoto kay ano tas bobo naman bumoto kay ano parang mga ratbu mag isip eh',
    'puro nalang pang g@g@go at katarantaduhan ang nangyayare ngayon eleksyon tangin@',
    'shet may tanga na nagbabasa neto oh mukhang bobo HAHAHAHAHA ',
    'ang mahalaga mukha kang burat na gago paka hinayupak mo',
    'tangina mag bayad ka naman ng utang mo parang ng gago mo na ako nyan eh kala mo sakin tanga',
    'mawawala na daw ang earth pag tapos ng limang taon tangina gago bobo ayoko pa mamatay',
    ],
    [ 
    'may 8oB0 na nakatingin sayo t@nga oh parang ulul ka daw sabi ni gagu',
    'kapag ramdam niyong gago kasama niya gaguhin nyo din para magalit si tanga ma uulul yun',
    'putangina ang inet put@ngina put@ng1na',
    'ang pogi 6@go taena bat ganun tas ako panget kinginang yan',
    'ang sama mo pakyu ka parang hindi ka kaibigan @mpota paka u1u1 pakyu!',
    'ang hirap mag isip putangina ayoko na pang bobo to taena pakyu kayo',
    'b00r@@t ka ba Kupal ampota kala nakakatawa siya eh parang gago lang naman',
    'nag sama sama sila bobo tanga hinayupak pakyu sa pag lalakbay papuntang russia',
    'ang hirap mabuhay sa pinas tangina nakakahiya ang mga burat tila tanga ampota',
    'bakit ba para kang tanga bobo burat tangina ka',
    ],

    [
    'busog pa ako parang gago ampota inutil tarando tangina',
    'si b0b0 si t@nga si t@n6in@ si burat si ulul',
    'nag sama sama sila bobo tanga hinayupak pakyu tarantado sa pag lalakbay papuntang russia',
    'hirap ng may sakit t@ng!n@ laging kapos sa pera @mp00t@ pang b0b0 na buhay to pakyu inamo',
    'puro naman mura tong gago na to eh tangina mo po pakyu kadin po at shet ka ampota',
    'ang galing ni gago lumangoy panis si tanga at tarantado pero humahabol si gunggong kay burat oh',
    'ako si bobo tanga inutil gunggong tarantado salvador',
    'ayaw ko sayo tang!na mo pakyu ul00l tarantado gungg00ng',
    'may gusto daw manligaw sayo kaso g@@go0 t@@r*nt*do b-0-b-o t@ng@ at kup@l ung tao',
    'sarap kumain ng b00b0 lasang tanga @mpvta tas amoy t@r@ntad0ng k!ng!na',
    ],
    [
    'puro na mura to t@ng@ 1nutil gungg0n6 t@ng1na burat b0b0',
    'nagkasakit pa ako putangina naman apaka bobo ng buhay kingina puta pakyu ulul',
    'si b0b0 si t@ng@ si gag0 si tarantad0 si bur@t si inutil',
    'may anim na magkakaibigan sila gunggong tarantado putangina bobo tanga at hinayupak',
    'naglakbay sila gung60ng, T@r@nt@d0, put@n61na, obob, t@ng@, at h1nayup@k',
    'sama sama inakyat ni bobo, tanga, inutil, mangmang, ulul, at puta ang bundok tralala',
    'sabi ni bobo kay tanga ay wag siyang mag kupal kay tarantado kasi yari siya sa putangina mo ulul',
    'sinampal ni bobo si tanga tas sinuntok ni t@ng@ si puta para si hinayupak naman ang magalit kay tarantad0',
    'ang hirap kasama ni b0b0 putapakyu hinayupak ulul tarantado sa mall',
    'parang kakalabas lang ni ul0l sa presinto kasama si kin6In@ dahil sa pag sunod neto kay b0b0 at t@nga na taga sunod ni shet at ratbu'
    ],
    [
    'si kupal si puta si tarantado si gago si bobo si tangina si pakyow',
    'naglakbay ulit si p@ky0w si t@ng1n@ si obob si gag0 si t@r@ntad0 si ul0l at si put@ papuntang cubao',
    'nakakadismaya kasama ang mga putanginang yan lalakas mang gago ampota kala mo walang pinagaralan ang mga bobo tanga mangmang ulul',
    'ang sakit ng likod ko tangina nyo lahat mga bobo ulul gunggong hinayupak tarantado burat',
    'burat ka ba? Lakas ng tama mong ulul ka ah hindi mo ba alam na puro gago, tarantado, at kupal mga tao dito? Kung gusto mo pa mabuhay tangina mo umalis kana dito gago',
    'sabi ni g@g0 kay t@nga kumain siya ng bur@t kasabay si b0b0 kasi malapit na daw si putangina at kingina makauwi ng bahay mga ul0l',
    'bakit pa ako gagalaw eh nandyan naman kayo nila b0b0, hin@yup@k, ul0l, t@rant@d0, bur@t, tang@ at suso',
    'laki ng suso ni ano oh sarap lamasin ng suso ni ano oh.. Tangina nyo mga bunganga niyo talaga mga tarantado ampota di na nadala ang mga bobo na to t@ng1n@',
    'sabi ko naman sayo ang bobo tanga inutil gago hinayupak putangina tarantado si binay',
    'laki ng kup@I ni ano oh sarap lamasin ng 0bob ni ano oh.. T@ng1n4 nyo mga bunganga niyo talaga mga t@r4ntad0 @mp0t4 di na nadala ang mga 8o8o na to t@ng1n@'

    ],
    
]
def average(score_list):
    return round(sum(score_list) / len(score_list), 4)

def test(test_list):
    all_average = []
    
    for test in test_list:
        per_test_time = []
        
        for t in test:
            start = time.time()
            res = clean_text(t)
            end = time.time()
            duration =  end - start
            per_test_time.append(duration)
        all_average.append(average(per_test_time))
    return all_average
result = test(test_case)

print(result)

