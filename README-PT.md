[English](README.md)

# PestoWiki
Client multiplataforma para wikis feito com Python usando PySide6 (QT).

_PestoWiki é majoritariamente testado na minha instância da Mediawiki, os atalhos padrão são pensados para MediaWiki, mas podem ser alterados se necessário. Qualquer incompatibilidade com DokuWiki, ou qualquer outro software de wiki, pode ser adicionada na seção issues desse repositório._

![Screenshot_20250628_172806](https://github.com/user-attachments/assets/0d5afeba-cfd3-403a-8405-b3f4a0153645)

## TODO
 - [x] Atalhos de edição (negrito, códiho, etc...)
 - [x] Modo de navegação/edição (muda user-select)
 - [x] Atalhos de edição customizados
 - [x] Configurações
 - [x] Mudar endereço da wiki
 - [x] Opção para abrir links externos no navegador do sistema
 - [x] Menu 'ir' (barra de pesquisa)
 - [x] Traduções
 - [x] Injetar JS customizado
 - [x] Biblioteca JS padrão para interagir com wikis
 - [x] Favoritos
 - [x] Procurar por atualizações
 - [x] Botão de compartilhamento (_Navegação > Copiar link da página atual_)

## Como compilar
- Clone o repositório e instale `requirements.txt` em um venv (opcional) usando:
```
python -m venv .venv
pip install -r requirements.txt
```
- Gere `resources.py` usando `buildresource.sh`. (Funciona no Git Bash para Windows.)

## Empacotando

<img src="https://github.com/user-attachments/assets/86185670-548b-49ce-b14e-2b8652855660" width="150" align="right"/>

### AppImage
Para empacotar Pesto em um AppImage, você precisará do AppImageTool. Para empacotar rode `yourappimagetool.AppImage PestoWiki.AppDir`, isso vai gerar um arquivo AppImage sem nenhuma dependência, se quiser, você pode encontrar alguma forma de empacotá-las (crie um AppImage do resultado do PyInstaller - guia abaixo). O sistema rodando o AppImage precisará dos módulos `PySide6` e `requests` instalados.

### Com o PyInstaller
PyInstaller vai gerar uma pasta GRANDE (~400mb) com um unico binário e uma pasta que deve ser distribuida junto com ele para que a aplicação funcione (você pode empacotar as dependências no binário, mas isso tem um imenso imapcto na performance, já que será necessário desempacotar tudo na hora de rodar a aplicação). O repositório já tem um arquivo `spec` que é usado pelo PyInstaller para gerar a aplicação, você pode empacotar ele com o comando a seguir:
```
python -m PyInstaller pesto.spec
```
O resultado estará em `./dist`.

### Para usuários do MacOS
Não posso suportar o MacOS agora pois a Apple não oferece nenhum ambiênte favorável fora dos iDevices. Esteja livre para me informar de builds próprias para MacOS e eu as listarei aqui.
