import pandas as pd
from heapq import nlargest
from operator import itemgetter
import csv
from django.db import connection

##load data
class buildModel():
	def naiveBayes(self):  
		with connection.cursor() as cursor:
			cursor.execute("SELECT * from submissions")
			submissions_df = cursor.fetchall()
			cursor.execute("SELECT * from challenges")
			challenges_df = cursor.fetchall()

		##list all challenges  
		##building a model for a particular contest
		challendes_vld = challenges_df[challenges_df['contest_id']=='c8ff662c97d345d2']['challenge_id'].tolist()
		challendes_vld = set(challendes_vld)

		##generate challenge frequancy table
		challenges_top=submissions_df[submissions_df['contest_id']=='c8ff662c97d345d2'][['hacker_id','challenge_id']].drop_duplicates()['challenge_id'].value_counts().to_dict()

		##hacker's submissions
		users_submissions = submissions_df.groupby('hacker_id')['challenge_id'].apply(set)
		##harker's solved
		users_solved = submissions_df[(submissions_df['solved']==1)& (submissions_df['contest_id']=='c8ff662c97d345d2')].groupby('hacker_id')['challenge_id'].apply(set)
		##harker's unsolved(may solved lately)
		uusers_solved = submissions_df[(submissions_df['solved']==0) & (submissions_df['contest_id']=='c8ff662c97d345d2')].groupby('hacker_id')['challenge_id'].apply(set)

		##Create cohort pair count
		graph={}
		for hackerID, challenges in users_submissions.iteritems():
			add_graph(graph,challenges,challendes_vld)
			
		##Create cohort predict
		users_cohort={}
		for hackerID, challenges in users_submissions.iteritems():
			coh={}
			for clg in challenges:
				if clg in graph:
					temp_set=graph[clg]
					#print(temp_set)
					for cl, cnt in temp_set.items():
						#if cl not in users_solved.get(hackerID,{}):
						if cl in coh:
							coh[cl]=coh[cl]+cnt
						else:
							coh[cl]=cnt
			users_cohort[hackerID]=coh

		##Create solved cohort predict
		users_cohort_slv={}
		for hackerID, challenges in users_solved.iteritems():
			coh={}
			for clg in challenges:
				if clg in graph:
					temp_set=graph[clg]
					#print(temp_set)
					for cl, cnt in temp_set.items():
						#if cl not in users_solved.get(hackerID,{}):
						if cl in coh:
							coh[cl]=coh[cl]+cnt
						else:
							coh[cl]=cnt
			users_cohort_slv[hackerID]=coh

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

		for hackerID, challenges in users_submissions.iteritems():
			out.write(hackerID)
			filled=[]
			
			i=0
			for clg in uusers_solved.get(hackerID,{}):
				if clg not in users_solved.get(hackerID,{}):
					out.write(',')
					out.write(clg)
					i += 1
					if i >= 10:
						break
			
			
			total=create_top(users_cohort_slv.get(hackerID,{}), filled, out, 10, users_solved.get(hackerID,{}))
			total=create_top(users_cohort[hackerID], filled, out, 10, users_solved.get(hackerID,{}))
			total=create_top(challenges_top, filled, out, 10, users_solved.get(hackerID,{}))
			out.write('\n')
		out.close

			
			