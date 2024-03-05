import gitlab
GITLAB_URL = 'https://gitlab.com/'
GITLAB_TOKEN = 'glpat-'
REPO_NAME = 'git_auto'
BRANCHES = ['dev', 'test']
FOLDERS = ['gitlab', 'github', 'bitbucket']

# Подключение к GitLab
gl = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_TOKEN)
gl.auth()

# Проверка существования репозитория
def check_repository_exists(name):
    try:
        return gl.projects.get(name)
    except gitlab.exceptions.GitlabGetError as e:
        return None

# Создание репозитория или получение существующего
def get_or_create_repository():
    repo = check_repository_exists(REPO_NAME)
    if not repo:
        repo = gl.projects.create({'name': REPO_NAME})
    return repo

# Создание веток
def create_branches(repo):
    existing_branches = {branch.name for branch in repo.branches.list()}
    for branch in BRANCHES:
        if branch not in existing_branches:
            repo.branches.create({'branch': branch, 'ref': 'main'})

# Добавление папок
def add_folders(repo):
    for folder in FOLDERS:
        repo.files.create({'file_path': folder + '/README.md', 'branch': 'main', 'content': 'Initial commit', 'commit_message': 'Add ' + folder})

# Получение или создание репозитория
repo = get_or_create_repository()

# Создание веток
create_branches(repo)

# Добавление папок (если они есть)
if FOLDERS:
    add_folders(repo)

print("Репозиторий создан и настроен успешно.")
print("Ссылка на репозиторий:", repo.web_url)
