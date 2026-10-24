from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle


# PALETA INDUSTRIAL
FUNDO = (0.04, 0.07, 0.13, 1)
PAINEL = (0.09, 0.13, 0.22, 1)
CAMPO = (0.04, 0.07, 0.13, 1)
AZUL = (0.20, 0.55, 1, 1)
BRANCO = (0.94, 0.96, 0.98, 1)
CINZA = (0.69, 0.69, 0.69, 1)
VERMELHO = (0.75, 0.20, 0.17, 1)
BOTAO_LIMPAR = (0.19, 0.25, 0.36, 1)
PRETO = (0, 0, 0, 1)

class BotaoIndustrial(Button):

    def __init__(self, cor_fundo=AZUL, **kwargs):
        super().__init__(**kwargs)

        self.cor_fundo = cor_fundo
        self.background_normal = ""
        self.background_color = (0, 0, 0, 0)
        self.color = BRANCO
        self.bold = True

        with self.canvas.before:
            self.cor_canvas = Color(*self.cor_fundo)
            self.fundo = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[50]
            )

        self.bind(
            pos=self.atualizar_fundo,
            size=self.atualizar_fundo
        )

        self.bind(
            state=self.atualizar_cor
        )

    def atualizar_fundo(self, *args):
        self.fundo.pos = self.pos
        self.fundo.size = self.size

    def atualizar_cor(self, *args):
        if self.state == "down":
            self.cor_canvas.rgba = (
                self.cor_fundo[0] * 0.75,
                self.cor_fundo[1] * 0.75,
                self.cor_fundo[2] * 0.75,
                1
            )
        else:
            self.cor_canvas.rgba = self.cor_fundo


class CampoIndustrial(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(*PAINEL)
            self.fundo = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[12]
            )

        self.bind(
            pos=self.atualizar_fundo,
            size=self.atualizar_fundo
        )

    def atualizar_fundo(self, *args):
        self.fundo.pos = self.pos
        self.fundo.size = self.size


class CalculadoraHorarios(App):

    def build(self):
        Window.clearcolor = FUNDO

        tela = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=12
        )

        # CABEÇALHO
        cabecalho = BoxLayout(
            orientation="vertical",
            size_hint=(1, 0.19),
            spacing=2
        )

        titulo = Label(
            text="CALCULADORA\nDE TEMPO",
            font_size=105,
            bold=True,
            color=AZUL,
            halign="center",
            valign="middle"
        )

        subtitulo = Label(
            text="",
            font_size=20,
            color=CINZA
        )

        cabecalho.add_widget(titulo)
        #cabecalho.add_widget(subtitulo)
        tela.add_widget(cabecalho)
        
        # IMAGEM DO RELÓGIO
        relogio = Image(
            source="relogio.png",
            size_hint=(1, 0.15),
            allow_stretch=True,
            keep_ratio=True
        )

        tela.add_widget(relogio)

        # CAMPO DE HORÁRIO INICIAL
        tela.add_widget(Label(
            text="HORÁRIO INICIAL",
            font_size=100,
            bold=True,
            color=CINZA,
            size_hint=(1, 0.08),
            halign="left",
            valign="middle"
        ))

        self.inicio = TextInput(
            hint_text="Exemplo: 0800",
            multiline=False,
            font_size=100,
            halign="center",
            input_filter="int",
            foreground_color=PRETO,
            hint_text_color=CINZA,
            background_normal="",
            background_active="",
            background_color=BRANCO,
            cursor_color=AZUL,
            padding=[10, 12],
            size_hint=(1, 0.06)
        )
        tela.add_widget(self.inicio)

        # CAMPO DE HORÁRIO FINAL
        tela.add_widget(Label(
            text="HORÁRIO FINAL",
            font_size=100,
            bold=True,
            color=CINZA,
            size_hint=(1, 0.08),
            halign="left",
            valign="middle"
        ))

        self.fim = TextInput(
            hint_text="Exemplo: 1730",
            multiline=False,
            font_size=100,
            halign="center",
            input_filter="int",
            foreground_color=PRETO,
            hint_text_color=CINZA,
            background_normal="",
            background_active="",
            background_color=BRANCO,
            cursor_color=AZUL,
            padding=[10, 12],
            size_hint=(1, 0.06)
        )
        tela.add_widget(self.fim)

        # BOTÕES LADO A LADO
        botoes = BoxLayout(
            orientation="horizontal",
            spacing=12,
            size_hint=(1, 0.1)
        )

        botao_calcular = BotaoIndustrial(
            text="CALCULAR",
            font_size=100,
            cor_fundo=AZUL,
            color=FUNDO
        )
        botao_calcular.bind(
            on_press=self.calcular
        )

        botao_limpar = BotaoIndustrial(
            text="LIMPAR",
            font_size=100,
            cor_fundo=BOTAO_LIMPAR
        )
        botao_limpar.bind(
            on_press=self.limpar
        )

        botoes.add_widget(botao_calcular)
        botoes.add_widget(botao_limpar)
        tela.add_widget(botoes)

        # PAINEL DO RESULTADO
        self.resultado = Label(
            text="Digite os horários acima",
            font_size=90,
            bold=True,
            color=AZUL,
            halign="center",
            valign="middle",
            size_hint=(1, 0.25)
        )

        tela.add_widget(self.resultado)

        return tela

    def converter_horario(self, horario):

        if not horario.isdigit() or len(horario) != 4:
            raise ValueError(
                "Digite exatamente\n4 numeros!"
            )

        horas = int(horario[:2])
        minutos = int(horario[2:])

        if not (0 <= horas <= 23):
            raise ValueError(
                "Hora deve estar\nentre 00 e 23!"
            )

        if not (0 <= minutos <= 59):
            raise ValueError(
                "Minutos devem\nestar entre 00 e 59!"
            )

        return horas * 60 + minutos

    def calcular(self, botao):
        try:
            inicio = self.inicio.text.strip()
            fim = self.fim.text.strip()

            minutos_inicio = self.converter_horario(
                inicio
            )

            minutos_fim = self.converter_horario(
                fim
            )

            # Considerar passagem pela meia-noite
            if minutos_fim < minutos_inicio:
                minutos_fim += 24 * 60

            total = minutos_fim - minutos_inicio

            horas = total // 60
            minutos = total % 60
            decimal = total / 60

            inicio_formatado = (
                f"{inicio[:2]}:{inicio[2:]}"
            )

            fim_formatado = (
                f"{fim[:2]}:{fim[2:]}"
            )

            self.resultado.color = AZUL

            self.resultado.text = (
                f"INÍCIO: {inicio_formatado}\n"
                f"FINAL: {fim_formatado}\n"
                f"TEMPO: {horas}h {minutos:02d}min\n"
                f"{decimal:.2f} HORAS"
            )

        except ValueError as erro:
            self.resultado.color = (
                1, 0.35, 0.30, 1
            )
            self.resultado.text = (
                f"ERRO\n{erro}"
            )

    def limpar(self, botao):
        self.inicio.text = ""
        self.fim.text = ""

        self.resultado.color = AZUL
        self.resultado.text = "Digite os horários acima"


CalculadoraHorarios().run()
