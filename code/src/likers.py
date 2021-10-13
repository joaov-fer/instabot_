from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import random

my_username = '_my_username'
perfil = 'username_to_search'

lista_negra = [
    'usernames_black_list'
]
scrolls = 60

letras_permitidas = [
    'a',
    'e',
    'i'
]

nomes_permitidos = [
    'beatriz'
]


browser = webdriver.Chrome(ChromeDriverManager().install())
browser.implicitly_wait(10)

browser.get("https://www.instagram.com/")

sleep(3)
username_input = browser.find_element_by_css_selector("input[name='username']")
password_input = browser.find_element_by_css_selector("input[name='password']")
sleep(1.5)
username_input.send_keys(my_username)
sleep(3)
password_input.send_keys("my_password")
sleep(1)
login_button = browser.find_element_by_xpath("//button[@type='submit']")
login_button.click()
sleep(3)


# <-------------------------------
browser.get("https://www.instagram.com/"+perfil+"/")
sleep(2)
browser.find_element_by_xpath("//a[@href= \"/" + perfil + "/followers/\"" + "]").click()
sleep(1)
browser.find_element_by_class_name('PZuss').click()


for _ in range(1, scrolls):
    try:
        browser.execute_script('''
            var fDialog = document.querySelector('div[role="dialog"] .isgrP');
            fDialog.scrollTop = fDialog.scrollHeight
        ''')
        sleep(0.8)
    except Exception:
        continue

hrefs_na_tela = browser.find_elements_by_xpath('//div[@class="uu6c_"]')
sleep(15)

num_curtidas = 0

# url - nome
seletivos = []

for href in hrefs_na_tela:

    nome = href.find_element_by_xpath('.//div[@class="wFPL8 "]').text
    link = href.find_element_by_xpath('.//a[@class="FPmhX notranslate  _0imsa "]').get_attribute('href')
    username = href.find_element_by_xpath('.//a[@class="FPmhX notranslate  _0imsa "]').text

    if username != my_username:
        if  href.find_element_by_xpath('.//div[@class="Pkbci"]/button').text.lower() == 'seguindo':
            print(link + ' - ' + nome + ' [seguindo]')

        else:

            if username not in lista_negra:

                first_name = nome.split(' ')[0].lower()
                ultima_letra = first_name[-1:]

                if ultima_letra in letras_permitidas or first_name in nomes_permitidos:
                    print(link + ' - ' + nome + ' [aprovado]')
                    seletivos.append(link + '-' + nome)


print('---------------------------------')
print('Processados: ' + str(len(hrefs_na_tela)))
print('Selecionados: ' + str(len(seletivos)))


for selecionado in seletivos:

    infos = selecionado.split('-')
    link = infos[0]
    nome = infos[1]

    browser.get(link)

    primeira_foto = None
    try:
        primeira_foto = browser.find_element_by_css_selector('#react-root > section > main > div > div._2z6nI > article > div > div > div:nth-child(1) > div:nth-child(1) > a')
    except Exception:
        print(link + ' - ' + nome + ' [private]')
        continue

    if primeira_foto is not None:
        print(link + ' - ' + nome)
        sleep(random.randint(2, 5))

        primeira_foto = primeira_foto.get_attribute('href')
        browser.get(primeira_foto)
        sleep(2)
        if browser.find_element_by_css_selector('span > svg').get_attribute('aria-label') == 'Curtir':

            sleep(random.randint(6, 11))
            browser.find_element_by_xpath('//*[@class="fr66n"]/button').click()

            num_curtidas + 1

        sleep(random.randint(10, 30))
    else:
        sleep(1)
    # break

print('Curtidas: ' + str(num_curtidas))
browser.close()

