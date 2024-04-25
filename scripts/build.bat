
docker build .\jupyter-findjob-tryout -t jupyter-findjob-tryout
docker tag jupyter-findjob-tryout 192.168.10.61:5000/jupyter-findjob-tryout
docker push 192.168.10.61:5000/jupyter-findjob-tryout
