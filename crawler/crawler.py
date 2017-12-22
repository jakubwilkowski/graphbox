import pytz
from github import Github, GithubException
from py2neo import Graph, authenticate, Node, Relationship

from core.models import Repository, Developer, Language, Module, ModuleVersion
from graphbox.settings import UNWANTED_REPO_NAMES, NEO4J_PASS, NEO4J_USER, GITHUB_USER, GITHUB_PASS

# authenticate('localhost:7474', NEO4J_USER, NEO4J_PASS)
# graph = Graph("http://localhost:7474/")

class GitCrawler(object):

    @staticmethod
    def populate_repos(org_name='10clouds'):
        g = Github(GITHUB_USER, GITHUB_PASS)
        organization = g.get_organization(org_name)
        for repo in organization.get_repos():
            if not repo.private and not repo.fork and repo.name not in UNWANTED_REPO_NAMES:
                current_repo, _ = Repository.objects.update_or_create(name=repo.name,
                                                                      defaults={'created_at':
                                                                                    repo.created_at.replace(tzinfo=pytz.UTC)})

                GitCrawler.populate_developers(current_repo, repo)
                GitCrawler.populate_languages(current_repo, repo)
                GitCrawler.populate_modules(current_repo, repo)


    @staticmethod
    def populate_developers(current_repo, repo):
        for dev in repo.get_contributors():
            current_dev, _ = Developer.objects.update_or_create(login=dev.login,
                                                                defaults={'created_at':
                                                                              dev.created_at.replace(tzinfo=pytz.UTC),
                                                                          'name': dev.name,
                                                                          'location': dev.location})

            current_repo.contributors.add(current_dev)

    @staticmethod
    def populate_languages(current_repo, repo):
        for lang in repo.get_languages():
            current_lang, _ = Language.objects.update_or_create(name=lang)

            current_repo.languages.add(current_lang)

    @staticmethod
    def populate_modules(current_repo, repo):
        try:
            req_file = repo.get_contents('requirements.txt')
            deps = req_file.decoded_content.decode('utf-8').strip().split('\n')
            print(current_repo.name)
            print(deps)
            if deps:
                python = Language.objects.get(name='Python')
                for module in list(map(lambda x: x.split('=='), deps)):
                    current_module = Module.objects.update_or_create(name=module[0], language=python)
                    if len(module) > 1:
                        ModuleVersion.objects.create(module=current_module, repository=current_repo, version=module[1])
        except GithubException:
            pass

    @staticmethod
    def populate_graph():
        graph.delete_all()
        GitCrawler.populate_graph_nodes()
        GitCrawler.populate_graph_relations()

    @staticmethod
    def populate_graph_nodes():
        for repo in Repository.objects.all():
            new_node = Node('Repository', name=repo.name, created_at=str(repo.created_at))
            graph.create(new_node)

        for dev in Developer.objects.all():
            new_dev = Node('Developer', name=dev.login, login=dev.login, created_at=str(dev.created_at))
            graph.create(new_dev)

        for lang in Language.objects.all():
            new_lang = Node('Language', name=lang.name)
            graph.create(new_lang)

    @staticmethod
    def populate_graph_relations():
        for repo in Repository.objects.all():
            try:
                repo_node = graph.find(label='Repository', property_key='name', property_value=repo.name).__next__()
            except StopIteration:
                pass
            for dev in repo.contributors.all():
                try:
                    dev_node = graph.find(label='Developer', property_key='login', property_value=dev.login).__next__()
                except StopIteration:
                    pass
                repo_dev_rel = Relationship(dev_node, 'DEVELOPED', repo_node)
                graph.create(repo_dev_rel)

        for repo in Repository.objects.all():
            try:
                repo_node = graph.find(label='Repository', property_key='name', property_value=repo.name).__next__()
            except StopIteration:
                pass
            for lang in repo.languages.all():
                try:
                    lang_node = graph.find(label='Language', property_key='name', property_value=lang.name).__next__()
                except StopIteration:
                    pass
                repo_dev_lang = Relationship(repo_node, 'USES', lang_node)
                graph.create(repo_dev_lang)
