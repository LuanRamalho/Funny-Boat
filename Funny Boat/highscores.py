import pygame
import os
import json
from locals import *
from water import Water
import util
import cloud

class Highscores:
    def __init__(self, screen, new_score=-1, endless=False):
        self.screen = screen
        self.pathname = ""

        # Determinar o diretório de dados
        try:
            self.pathname = os.environ["HOME"] + "/.funnyboat"
        except KeyError:
            try:
                self.pathname = os.environ["APPDATA"] + "/Funny Boat"
            except KeyError:
                print("Couldn't get environment variable for home directory")
                self.pathname = "."
        if not os.path.exists(self.pathname):
            os.mkdir(self.pathname)

        # Nome do arquivo
        self.filename = os.path.join(
            self.pathname, "endless_scores.json" if endless else "scores.json"
        )

        # Inicializar *high scores*
        self.scores = []  # Inicialização para evitar erros de atributo
        self.scores = self.load_scores()

        self.done = False

        # Configurar fonte e imagem
        self.font = util.load_font("Cosmetica", 14)
        self.title_font = util.load_font("Cosmetica", 28)
        self.title = self.title_font.render("High Scores", True, (0, 0, 0))
        self.sky = util.load_image("taivas")

        # Verificar novo *high score*
        self.inputting = False
        self.input_score = -1
        if new_score > self.scores[-1]["score"]:
            self.inputting = True
            for i in range(10):
                if self.scores[i]["score"] < new_score:
                    self.input_score = i
                    self.scores.insert(i, {"name": "", "score": new_score})
                    self.scores = self.scores[:10]  # Garantir no máximo 10 *high scores*
                    self.write_scores()  # Salva imediatamente após a alteração do placar
                    break

    def load_scores(self):
        """Carrega os *high scores* de um arquivo JSON ou cria uma lista padrão."""
        if not os.path.exists(self.filename):
            return self.dummy_scores()

        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print("Failed to load high scores. Creating default scores.")
            return self.dummy_scores()

    def write_scores(self):
        """Salva os *high scores* no arquivo JSON."""
        try:
            with open(self.filename, "w") as f:
                json.dump(self.scores, f, indent=4)
        except IOError:
            print(f"Failed to write high scores to file {self.filename}")
            self.done = True

    def dummy_scores(self):
        """Cria uma lista padrão de *high scores*."""
        self.scores = [
            {"name": "Funny Boat", "score": 2000},
            {"name": "Hectigo", "score": 1500},
            {"name": "JDruid", "score": 1000},
            {"name": "Pekuja", "score": 750},
            {"name": "Pirate", "score": 500},
            {"name": "Shark", "score": 400},
            {"name": "Seagull", "score": 300},
            {"name": "Naval mine", "score": 200},
            {"name": "Cannonball", "score": 100},
            {"name": "Puffy the Cloud", "score": 50},
        ]
        self.write_scores()  # Gravar os dados iniciais no arquivo
        return self.scores

    def run(self):
        water = Water.global_water
        water_sprite = pygame.sprite.Group()
        water_sprite.add(water)
        while not self.done:
            self.screen.blit(self.sky, self.screen.get_rect())
            water.update()
            cloud.update()
            cloud.draw(self.screen)
            water_sprite.draw(self.screen)

            rect = self.title.get_rect()
            rect.centerx = self.screen.get_rect().centerx
            rect.top = 10

            self.screen.blit(self.title, rect)

            for i in range(10):
                color = (0, 0, 0)
                if self.inputting and self.input_score == i:
                    color = (220, 120, 20)
                score = self.scores[i]
                image = self.font.render(f"{i + 1}. {score['name']}", True, color)
                rect = image.get_rect()
                rect.top = 50 + i * 1.5 * rect.height
                rect.left = 10
                self.screen.blit(image, rect)

                image = self.font.render(str(score["score"]), True, color)
                rect = image.get_rect()
                rect.top = 50 + i * 1.5 * rect.height
                rect.right = self.screen.get_rect().right - 10
                self.screen.blit(image, rect)

            pygame.display.flip()

            nextframe = False
            while not nextframe:
                pygame.event.post(pygame.event.wait())
                for event in pygame.event.get():
                    if event.type == NEXTFRAME:
                        nextframe = True
                        continue
                    if self.inputting:
                        if event.type == QUIT:
                            self.inputting = False
                            self.write_scores()
                        if event.type == KEYDOWN:
                            if event.key in {K_RETURN, K_ESCAPE}:
                                self.inputting = False
                                self.write_scores()
                            elif event.key == K_BACKSPACE:
                                if len(self.scores[self.input_score]["name"]) != 0:
                                    self.scores[self.input_score]["name"] = self.scores[self.input_score]["name"][:-1]
                            elif event.unicode and len(self.scores[self.input_score]["name"]) < 32:
                                self.scores[self.input_score]["name"] += event.unicode
                    else:
                        if event.type in {KEYDOWN, QUIT, JOYBUTTONDOWN}:
                            self.done = True
                            nextframe = True
