from pintruyen import UserInfo, Session


def get_follows(request):
    email = request.form['e']
    password = request.form['p']
    
    sess = Session(UserInfo.fromCredential(email, password))
    comics = []

    page = 1

    while True:
        follow_page = sess.getFollows(page)
        if not len(follow_page): break
        comics.extend(follow_page)
        page += 1

    return "\n".join(map(lambda i: f"{i + 1}. {comics[i].name}{' - ' + comics[i].lastViewChapter.title if comics[i].lastViewChapter else ""}", range(len(comics))))