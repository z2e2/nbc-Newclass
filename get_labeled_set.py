import glob
import pickle
PATH = '/lustre/scratch/zz374/nbc_paper_year_simulation/{YEAR}/save_{FOLD_IDX}/*.dat'
labeled_dict = {}
for year in [2005, 2010, 2015, 2019]:
    labeled_dict[year] = {}
    for idx in range(1, 6):
        print(year, idx)
        sub_path = PATH.format(YEAR=str(year), FOLD_IDX=str(idx))
        labeled = glob.glob(sub_path)
        labeled_set = set([item.split('/')[-1].split('-')[0] for item in labeled])
        labeled_dict[year][idx] = labeled_set

pickle.dump(labeled_dict, open("labeled.pkl","wb"))
