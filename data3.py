#!/usr/bin/env python3
__author__ = "Group 16"
__version__ = 0.1
__license__ = "GPL v3.0"


def get_hash():
    r = re.compile(r'^    Fixes: [a-f0-9]+')
    f = open("result-fixes.txt","r")
    save = []
    hash = []
    for line in f:
        save.append(line)
    count = 0
    for i in range(len(save)):
        pas = save[i]
        if r.match(pas):
            if 6 < len(r.search(pas).group(0)[11::]) < 15:
                hash.append(r.search(pas).group(0)[11::])
                count += 1
        if count >= 200:
            break
    return hash


def get_date():
    r = open("result-date.txt","r")
    save = []
    date = []
    count = 0
    for line in r:
        save.append(line)

    for i in range(len(save)):
        pas = save[i][8:18]
        date.append(pas)
        count += 1
        if count >= 200:
            break
    return date


def gitFilebugs(repo):
    res = []
    hash = get_hash()
    for i in hash:
        cmd1 = ['git', 'show', i, '--pretty=format:%cd']
        p1 = Popen(cmd1, cwd=repo, stdout=PIPE,shell=False)
        data1, res1 = p1.communicate()
        res.append(data1.decode("utf-8").split("\n")[0][:10:])
    return res


def minus():
    date_bug = gitFilebugs("linux-stable")
    date_fix = get_date()
    res = []
    for i in range(len(date_bug)):
        db = datetime.strptime(date_bug[i],'%Y-%m-%d')
        df = datetime.strptime(date_fix[i],'%Y-%m-%d')
        res.append((df - db).days)
    mean = 0
    for i in res:
        mean += i
    m = mean/len(res)
    return m

if __name__ == '__main__':
    m = minus()
    print(m)
