import pandas as pd
from heapq import nlargest
from operator import itemgetter
import csv

##load data
class buildModel():
	def naiveBayes(self):  
		df_sbm = pd.read_csv('submissions.csv')
		df_clg = pd.read_csv('challenges.csv')

		##list all challenges under contest "c8ff662c97d345d2"
		vld_clg = df_clg[df_clg['contest_id']=='c8ff662c97d345d2']['challenge_id'].tolist()
		vld_clg = set(vld_clg)

		##generate challenge frequancy table
		top_clg=df_sbm[df_sbm['contest_id']=='c8ff662c97d345d2'][['hacker_id','challenge_id']].drop_duplicates()['challenge_id'].value_counts().to_dict()

		##harker's submissions
		sbm_hk = df_sbm.groupby('hacker_id')['challenge_id'].apply(set)
		##harker's solved
		slv_hk = df_sbm[(df_sbm['solved']==1)& (df_sbm['contest_id']=='c8ff662c97d345d2')].groupby('hacker_id')['challenge_id'].apply(set)
		##harker's unsolved(may solved lately)
		uslv_hk = df_sbm[(df_sbm['solved']==0) & (df_sbm['contest_id']=='c8ff662c97d345d2')].groupby('hacker_id')['challenge_id'].apply(set)

		##Create cohort pair count
		graph={}
		for hid, clgs in sbm_hk.iteritems():
			add_graph(graph,clgs,vld_clg)
			
		##Create cohort predict
		hk_coh={}
		for hid, clgs in sbm_hk.iteritems():
			coh={}
			for clg in clgs:
				if clg in graph:
					temp_set=graph[clg]
					#print(temp_set)
					for cl, cnt in temp_set.items():
						#if cl not in slv_hk.get(hid,{}):
						if cl in coh:
							coh[cl]=coh[cl]+cnt
						else:
							coh[cl]=cnt
			hk_coh[hid]=coh

		##Create solved cohort predict
		hk_coh_slv={}
		for hid, clgs in slv_hk.iteritems():
			coh={}
			for clg in clgs:
				if clg in graph:
					temp_set=graph[clg]
					#print(temp_set)
					for cl, cnt in temp_set.items():
						#if cl not in slv_hk.get(hid,{}):
						if cl in coh:
							coh[cl]=coh[cl]+cnt
						else:
							coh[cl]=cnt
			hk_coh_slv[hid]=coh

		##function to create cohort pair
		def add_graph(graph, sub_set, contest_set):
			for cid1 in sub_set:
				for cid2 in sub_set:
					if cid1 != cid2:
						if cid2 in contest_set:
							if cid1 in graph:
								temp = graph.get(cid1)
								if cid2 in temp:
									temp[cid2] = temp.get(cid2) + 1
								else:
									temp[cid2] = 1
								graph[cid1]=temp
							else:
								graph[cid1]={cid2:1}
			return

		##function to generate final csv
		def create_top(d, filled, out, n, solved):
			total = 0
			topitems = nlargest(n+len(solved), sorted(d.items()), key=itemgetter(1))
			for i in range(len(topitems)):
				if topitems[i][0] in filled:
					continue
				if topitems[i][0] in solved:
					continue
				if len(filled) == 10:
					break
				out.write(',' + topitems[i][0])
				filled.append(topitems[i][0])
				total += 1

			return total
			

		##Create predict csv
		out = open('result.csv', "w")

		for hid, clgs in sbm_hk.iteritems():
			out.write(hid)
			filled=[]
			
			i=0
			for clg in uslv_hk.get(hid,{}):
				if clg not in slv_hk.get(hid,{}):
					out.write(',')
					out.write(clg)
					i += 1
					if i >= 10:
						break
			
			
			total=create_top(hk_coh_slv.get(hid,{}), filled, out, 10, slv_hk.get(hid,{}))
			total=create_top(hk_coh[hid], filled, out, 10, slv_hk.get(hid,{}))
			total=create_top(top_clg, filled, out, 10, slv_hk.get(hid,{}))
			out.write('\n')
		out.close

			
			