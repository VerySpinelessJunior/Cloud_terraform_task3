# Cloud_terraform_task3
# "Семь бед, один ответ - костыль и велосипед"
Платформа для обучения языкам программирования, разворачивается с использованием terraform в облачном сервисе SberCloud



https://github.com/VerySpinelessJunior/Cloud_terraform_task3/assets/98365261/543acd51-3ba9-407c-b76e-f54e10eb7f11


# Requrements
1. terraform
2. Account cloud.advanced
3. open ssh

# How to set up
1. Установить тераформ по гайду из документации https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli
2. Создать папку проекта, положить туда файлы main.tf и terraform.tfvars
3. В файле terraform.tfvars указать в полях access_key и secret_key вашу пару ключей доступа, они получаются из панели вашего пользователя. В поле root_passwd указать желаемый пароль для root пользователя

![image](https://github.com/VerySpinelessJunior/Cloud_terraform_task3/assets/98365261/d18580f7-5b3b-4b86-8e7d-266bad30ebb4)

4. В папке проекта открыть терминал и проинициалировать провайдера командой terraform init (Для этого понадобиться VPN)
5. terraform apply в появившемя поле ввода вводим yes

![image](https://github.com/VerySpinelessJunior/Cloud_terraform_task3/assets/98365261/30fb2540-27ae-4ccc-abc3-dd80344ea9dd)


6. Дождаться окончания процесса
7. Зайти в консоль cloud.advance и перейти на страницу Elastic Cloud Service, там будут находиться 2 сервера.

![image](https://github.com/VerySpinelessJunior/Cloud_terraform_task3/assets/98365261/5ec4e87a-abde-4343-9571-d132d5a03976)

8. Копируем nat ip адресс (подсвечен синим и имеет другую подсеть)
9. С помощью ssh scp и полученного ранее ip адреса передаём баш скрипты на ECS, которые развернут систему
10. Подключаемся к серверам по shh и запускаем скрипты
11. profit
