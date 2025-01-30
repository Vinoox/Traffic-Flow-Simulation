import matplotlib.pyplot as plt
import numpy as np

# Dane
ids = ["(0,0)", "(0,1)", "(0,2)", "(0,3)", "(0,4)", "(0,5)", "(0,6)", "(0,7)", "(0,8)", "(0,9)",
       "(1,0)", "(1,1)", "(1,2)", "(1,3)", "(1,4)", "(1,5)", "(1,6)", "(1,7)", "(1,8)", "(1,9)",
       "(2,0)", "(2,1)", "(2,2)", "(2,3)", "(2,4)", "(2,5)", "(2,6)", "(2,7)", "(2,8)", "(2,9)",
       "(3,0)", "(3,1)", "(3,2)", "(3,3)", "(3,4)", "(3,5)", "(3,6)", "(3,7)", "(3,8)", "(3,9)",
       "(4,0)", "(4,1)", "(4,2)", "(4,3)", "(4,4)", "(4,5)", "(4,6)", "(4,7)", "(4,8)", "(4,9)",
       "(5,0)", "(5,1)", "(5,2)", "(5,3)", "(5,4)", "(5,5)", "(5,6)", "(5,7)", "(5,8)", "(5,9)",
       "(6,0)", "(6,1)", "(6,2)", "(6,3)", "(6,4)", "(6,5)", "(6,6)", "(6,7)", "(6,8)", "(6,9)",
       "(7,0)", "(7,1)", "(7,2)", "(7,3)", "(7,4)", "(7,5)", "(7,6)", "(7,7)", "(7,8)", "(7,9)",
       "(8,0)", "(8,1)", "(8,2)", "(8,3)", "(8,4)", "(8,5)", "(8,6)", "(8,7)", "(8,8)", "(8,9)",
       "(9,0)", "(9,1)", "(9,2)", "(9,3)", "(9,4)", "(9,5)", "(9,6)", "(9,7)", "(9,8)", "(9,9)"]

set1 = [1.0565832753976185, 7.741830888248625, 8.904669692244711, 8.890524774632127, 10.134958317113478, 10.08771260755252, 7.988806620792106, 8.218698763265841, 7.5700040957085175, 2.123566215688532, 6.545884656434012, 12.77417974519025, 15.273029748412677, 15.400858800986718, 18.082858091537428, 28.673845906283972, 15.78627360039863, 13.971140161156654, 11.794765205944286, 5.379282109372251, 6.916445264982623, 15.615337301594343, 17.38959690147543, 22.22588217038278, 33.186858223145265, 66.45208216704617, 29.411303240060807, 22.726883852514323, 32.707285507944704, 5.54293483984275, 8.407385481142365, 19.696057112393866, 29.296718539387346, 29.111606281844352, 47.77270331292971, 42.95595676856053, 20.72528672066946, 17.665090462120858, 95.28845374798259, 7.000529741554104, 10.263510813713074, 22.729916015983875, 34.63499999654819, 24.30076097537364, 57.165694571458374, 47.211100740774775, 22.51984447462683, 44.14915512117107, 86.488596335598, 25.65144650397762, 10.135052517056465, 20.27255839314954, 37.78725331448258, 16.877381819050488, 49.64227321421916, 36.94761299078281, 25.84694707989693, 71.43374884345315, 61.42113658703036, 38.20371560113771, 8.872438623949334, 18.86639299500027, 25.670644157870687, 56.478607097304014, 65.78301677356164, 49.184827952877455, 35.42424901489638, 19.312280416488647, 52.22122101288922, 13.13478286777224, 8.047437656159495, 19.430090849613627, 21.12692080838706, 51.26430485834622, 82.63884207445705, 31.95651264744258, 38.38201783931078, 19.775700820244825, 23.109582379624083, 7.414812464663323, 7.80796580016613, 14.40378760403775, 15.440345187671483, 18.67893692325143, 17.338087991859673, 23.530296917048105, 16.94083566518174, 15.492805171703946, 12.827590195859065, 6.283276146704997, 3.716127248037429, 7.594316378804564, 9.124467424724413, 10.033575239388838, 8.754900533612036, 7.599579885474637, 9.957722680909294, 10.683007264623837, 7.502402329663618, 3.113219829706045]

set2 = [0.6882099807262421, 4.983797384345013, 2.9832378029823303, 3.8979877204429814, 3.08113555575526, 5.631211116200402, 5.9546036422252655, 4.994937976201375, 5.047373338179155, 2.6152095794677734, 3.9368407924969993, 5.622066375685901, 5.801025114276192, 6.103271830826998, 6.5124896401944365, 6.738538488974938, 7.859552288955113, 7.903990745544434, 5.9876599198295954, 4.479819941520691, 4.496145397424698, 7.67793374756972, 6.101847626946189, 6.219600869948605, 5.4341736479503355, 5.863932284755983, 7.850608507792155, 6.705258429050446, 6.162493169307709, 3.0751749321266457, 3.917690736276132, 8.58403434940413, 6.699231147766113, 8.17809886681406, 7.9768175393977065, 5.5080736890623845, 7.21851653211257, 9.417943381056, 7.583488481385367, 4.8839936834393125, 3.6519562772342136, 6.163135078218248, 5.284435592713903, 8.28867932883176, 7.945614130991809, 7.987662623910343, 10.97673255464305, 33.86148298870433, 7.46122917224621, 4.139510154724121, 5.0230833978363965, 7.579368150840371, 6.746043920516968, 8.526807829865025, 9.903908741885218, 8.994270066957217, 7.2641032596804065, 30.88350521455897, 6.241914310625622, 2.6436728619514627, 4.105690431594849, 9.468552055566207, 7.220103666186333, 7.961742770805787, 8.522667033331734, 7.331691270178937, 8.268969366627354, 7.893321209175642, 6.4863031751969284, 2.936595333947076, 4.6341392993927, 5.904484139038966, 6.847354716892484, 6.880176737904549, 7.474120823960555, 7.422490971429007, 7.077944111078978, 6.579317627808987, 8.461355981180223, 3.094861315142724, 4.498021861781245, 4.039050025098464, 7.927884878935637, 6.31361797704535, 5.612508139367831, 6.033922610860882, 6.234417791877474, 7.069406986236572, 7.108133203453487, 3.62179906744706, 3.915783315896988, 3.868917979692158, 4.387803673744202, 5.236988748822894, 5.773326086275505, 3.7298150062561035, 6.109251092981409, 7.804958164691925, 4.427727185762846, 0.0]

# Tworzenie wykresu
x = np.arange(len(ids))  # Pozycje na osi X
width = 0.35  # Szerokość słupków

fig, ax = plt.subplots(figsize=(20, 8))
rects1 = ax.bar(x - width / 2, set1, width, label='stały cykl świateł', color='blue')
rects2 = ax.bar(x + width / 2, set2, width, label='adaptacyjny cykl świateł', color='orange')


# Dodanie etykiet i tytułu
ax.set_xlabel('ID')
ax.set_ylabel('Średni czas oczekiwania na skrzyżowaniu')
ax.set_title('Porównanie średnich czasów oczekiwania (stały cykl świateł - adaptacyjny cykl świateł) 1000 pojazdów')
ax.set_xticks(x[::10])  # Wyświetlanie co 10. etykiety na osi X
ax.set_xticklabels(ids[::10], rotation=45)
ax.legend()

# Wyświetlenie wykresu
plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
import numpy as np

# Dane
set1 = [1.4592703311674056, 21.62307718525762, 14.679347325015712, 10.65687964791837, 34.99035355387902, 34.7499129423281, 108.18848653904443, 18.06960773904149, 8.784251776006487, 3.512018769979477, 9.915006729440952, 
34.3897223368935, 29.933473722475796, 44.909533652832835, 53.3395541530145, 41.436465775055744, 112.37804509742915, 38.39986650050913, 48.37377761432103, 13.967988859052243, 10.359649737299335, 44.2136516477852, 
27.614543461731696, 37.82446283939456, 62.208897082993154, 81.9200325077887, 123.39904575991484, 44.58394342900799, 47.05555913123217, 20.994064315672844, 38.36880876904442, 57.33888291120529, 41.33288869962973, 
42.83409739827742, 62.47387311229967, 46.79368906262992, 75.13825342564643, 90.17856645250187, 90.01933523889124, 14.47699325001655, 31.980596501380205, 40.27434727341208, 62.35170436730938, 78.59279948357342, 101.78093014761458, 87.42166546114593, 81.88580141224703, 130.8651272896255, 146.5305760140731, 88.66770971334722, 34.3907901571508, 29.21816736609996, 67.7014249265194, 63.08237616469463, 41.28573725938434, 56.02130862069705, 120.85431688490544, 90.89222792286219, 252.29892734948754, 99.54487309636663, 51.93134280314958, 40.6936434742799, 42.63884572654354, 89.09798475218491, 34.48220754205511, 33.999141576338786, 72.92064220358283, 50.60131628883076, 97.31396475444834, 18.704832363954353, 64.35214591992867, 48.61882840626992, 33.687972792464755, 164.60898049694583, 76.63631603524492, 116.4144026898608, 297.0314325576642, 90.56117106954432, 72.10050498861574, 20.65054611155861, 21.251564094985742, 85.69639303607326, 29.811293883483952, 143.89839758998468, 47.751111074955794, 32.19350013217411, 277.26963205458026, 30.869693923320167, 17.366124635101645, 17.339805690747387, 7.024040304381272, 11.129846334457397, 10.705057633928506, 19.11081047468288, 19.64695514417162, 13.21164810911138, 16.98093420327312, 14.899531445569462, 9.094572720989104, 5.108181317647298]
set2 = [1.0565832753976185, 7.741830888248625, 8.904669692244711, 8.890524774632127, 10.134958317113478, 10.08771260755252, 7.988806620792106, 8.218698763265841, 7.5700040957085175, 2.123566215688532, 6.545884656434012, 12.77417974519025, 15.273029748412677, 15.400858800986718, 18.082858091537428, 28.673845906283972, 15.78627360039863, 13.971140161156654, 11.794765205944286, 5.379282109372251, 6.916445264982623, 15.615337301594343, 17.38959690147543, 22.22588217038278, 33.186858223145265, 66.45208216704617, 29.411303240060807, 22.726883852514323, 32.707285507944704, 5.54293483984275, 8.407385481142365, 19.696057112393866, 29.296718539387346, 29.111606281844352, 47.77270331292971, 42.95595676856053, 20.72528672066946, 17.665090462120858, 95.28845374798259, 7.000529741554104, 10.263510813713074, 22.729916015983875, 34.63499999654819, 24.30076097537364, 57.165694571458374, 47.211100740774775, 22.51984447462683, 44.14915512117107, 86.488596335598, 25.65144650397762, 10.135052517056465, 20.27255839314954, 37.78725331448258, 16.877381819050488, 49.64227321421916, 36.94761299078281, 25.84694707989693, 71.43374884345315, 61.42113658703036, 38.20371560113771, 8.872438623949334, 18.86639299500027, 25.670644157870687, 56.478607097304014, 65.78301677356164, 49.184827952877455, 35.42424901489638, 19.312280416488647, 52.22122101288922, 13.13478286777224, 8.047437656159495, 19.430090849613627, 21.12692080838706, 51.26430485834622, 82.63884207445705, 31.95651264744258, 38.38201783931078, 19.775700820244825, 23.109582379624083, 7.414812464663323, 7.80796580016613, 14.40378760403775, 15.440345187671483, 18.67893692325143, 17.338087991859673, 23.530296917048105, 16.94083566518174, 15.492805171703946, 12.827590195859065, 6.283276146704997, 3.716127248037429, 7.594316378804564, 9.124467424724413, 10.033575239388838, 8.754900533612036, 7.599579885474637, 9.957722680909294, 10.683007264623837, 7.502402329663618, 3.113219829706045]

# Obliczanie sum
sum_set1 = sum(set1)
sum_set2 = sum(set2)

# Tworzenie wykresu
labels = ['Stały cykl świateł', 'Adaptacyjny cykl świateł']
sums = [sum_set1, sum_set2]

fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(labels, sums, color=['blue', 'orange'])

# Dodanie etykiet i tytułu
ax.set_ylabel('Suma średnich czasów oczekiwania')
ax.set_title('Porównanie sum średnich czasów oczekiwania')

# Wyświetlenie wykresu
plt.tight_layout()
plt.show()
