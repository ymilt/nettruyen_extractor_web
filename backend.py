from pintruyen import UserInfo, Session
from concurrent.futures import ThreadPoolExecutor, wait
import time


def get_follows(request):

    email = request.form['e']
    password = request.form['p']

    try:
        sess = Session(UserInfo.fromCredential(email, password))
    except:
        return ""

    load = {
        "run": True,
        "pages": 0
    }

    def proc_page(p):
        if not load["run"]:
            return
        follow_page = sess.getFollows(p)
        if not len(follow_page): 
            load["run"] = False
            return
        load[p] = follow_page
        load["pages"] += 1

    workers = 2
    wait_time = workers * 4.5

    with ThreadPoolExecutor(workers) as exe:
        i = 1
        while load["run"]:
            load["pages"] = 0
            ts = time.time()

            for _ in range(workers):
                exe.submit(proc_page, i + _)

            while load["run"] and load["pages"] < workers:
                if time.time() - ts > wait_time:
                    # Timeout
                    return ""
                time.sleep(.05)

            i += workers

    load.pop("run"), load.pop("pages")

    comics = []

    for key in sorted(load.keys()):
        comics.extend(load[key])

    return "\n".join(map(lambda i: f"{i + 1}. {comics[i].name}{' - ' + comics[i].lastViewChapter.title if comics[i].lastViewChapter else ''}", range(len(comics))))