pip3 freeze > requirements.txt

git add .

git commit -m $1

git push

scp -r abi Amiri-Regular.ttf Bookman-Italic.ttf Bookman.ttf DejaVuSansCondensed-Oblique.ttf DejaVuSansCondensed.ttf app .env requirements.txt DockerFile nasri@103.176.79.228:/home/nasri/HalalBC