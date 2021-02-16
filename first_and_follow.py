import argparse

def compute_first(rules):
	for rule in rules:
		if rule[4] == True:
			firsts = get_first(rule, rules)
			for el in firsts:
				rule[2].append(el)
				
				

def compute_follow(rules):
	rules[0][3].append('$')
	to_adds = []
	for rule in rules:
		if rule[4] == True:
			follows, to_add = get_follow(rule, rules)
			to_adds += to_add
			# print(follows)
			for el in follows:
				# print(el)
				rule[3].append(el)

	for x in to_adds:
		for rule in rules:
			if x[0] == rule[0]:
				for rule1 in rules:
					if x[1] == rule1:
						for n in rule1[3]:
							if n not in rule[3]:
								rule[3].append(n)


def get_follow(rule, rules):
	follows = []
	lit = rule[0]
	# print(lit)
	to_add = []

	for rule in rules:
		for rs in rule[1]:
			if lit in rs:
				rside = rs
				index = rs.find(lit)
				expression = rside[index:]
				if len(expression) == 1:
					for r in rules:
						if r[0] == rule[0]:
							if r[3] != [] and expression != rule[0]:
								follows+=r[3]
							else:
								if expression != rule[0]:
									to_add.append((lit, r))	
									# follows+=get_follow(r, rules)
				else:
					new_follows = return_follow(expression, rules)
					follows += new_follows
					while('epsilon' in new_follows):
						expression = expression[1:]
						if len(expression)==1:
							for r in rules:
								if r[0] == rule[0]:
									if r[3] != []:
										follows+=r[3]
									else:
										to_add.append((lit, r))	
									break
							break
						else:
							new_follows = return_follow(expression, rules)
							follows+=new_follows

	ret = list(set(follows))
	if 'epsilon' in ret:
		ret.remove('epsilon')				
	return ret, to_add				



def return_follow(expression, rules):
	follows = []
	lit = expression[1]
	if not lit.isupper():
		return [lit]
	for rule in rules:
		if rule[0] == lit:
			return rule[2]


def get_first(rule, rules):
	firsts = []
	add_epsilon = False		
	for rs in rule[1]:
		rside = rs
		if rside[0].isupper():
			new_firsts = return_first(rside, rules)
			firsts = firsts + new_firsts
			if 'epsilon' in firsts:
				firsts.remove('epsilon')
			while('epsilon' in new_firsts):
				# print(rside)
				if len(rside) == 1:
					new_firsts = return_first(rside, rules)
					# print(new_firsts)
					firsts+=new_firsts
					if 'epsilon' in new_firsts:
						add_epsilon = True
					break
				else:
					rside = rside[1:]
					new_firsts = return_first(rside, rules)
					firsts+=new_firsts
					if 'epsilon' in firsts:
						firsts.remove('epsilon')

		else:
			if rs == 'epsilon':
				firsts.append(rs)
			else:
				firsts.append(rs[0])

	if add_epsilon == True:
		# print(1111)
		firsts.append('epsilon')			
	return list(set(firsts))			




def return_first(rside, rules):
	firsts = []
	lit = rside[0]
	if not lit.isupper():
		return [lit]
	for rule in rules:
		if rule[0] == lit:
			rule[4] == False
			# print('_______')
			for rs in rule[1]:
				# print(rs)
				first_char = rs[0]
				if first_char.isupper():
					firsts = firsts + return_first(first_char, rules)		
				else:
					if rs == 'epsilon':
						firsts.append(rs)
					else:	
						firsts.append(first_char)	
									
	return list(set(firsts))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?",
                        metavar="file")

    args = parser.parse_args()

    print(args.file)

    rules = []
    rules1=[]
    with open(args.file) as f:
    	for line in f:
    		arr = line.split(':')
    		left_side = arr[0].replace(' ', '')
    		right = arr[1].replace(' ', '').replace('\n', '')
    		right_side = right.split('|')
    		firsts = []
    		follows = []
    		rule_temp = [left_side, right_side, firsts, follows, True]
    		rule = tuple(rule_temp)
    		rules.append(rule)
    		rules1.append(rule)

    	compute_first(rules)

    	
    	compute_follow(rules)

    	for rule in rules:
    		if rule[4] == True:
    			print(rule)

    	with open('task_5_1_result.txt', 'w') as f:
	    	for rule in rules:
	    		f.write(rule[0]+' : ')
	    		for right in rule[2]:
	    			f.write(right+' ')
	    		
	    		f.write(': ')
	    		for right in rule[3]:
	    			f.write(right+' ')
	    		f.write('\n')			

    	