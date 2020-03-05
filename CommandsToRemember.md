## To open the VENV for updating/modification
~/repoDir >>  
    `source RetailCrawler/.venv_hwms/bin/activate`

&nbsp;
## To Update PIP
~/repoDir >> {Activate VENV} >>  
    `pip install --upgrade pip`  

&nbsp;
## To list currrently installed PIP Packages
~/repoDir >> {Activate VENV} >>  
    `pip list`  

&nbsp;
## To Install new PIP Packages
~/repoDir >> {Activate VENV} >>  
    `pip install myNewPackage`

&nbsp;
## To update the `requirements.txt` file
~/repoDir >> {Activate VENV} >>  
    `pip freeze -r templateReqs.txt > newReqs.txt`
    
&nbsp;
## To Deactivate the Environment when finished
~/repoDir >> {Activate VENV} >>  
    `deactivate`  

&nbsp;

---

## To Create a ZIP with Library Contents
~/repoDir >>  
-    `cd v-env/lib/python3.8/site-packages` (*or `dist-packages`)  
-    `zip -r9 ${OLDPWD}/function.zip .`  
-    `cd $OLDPWD`  
-    `zip -g function.zip lambda_function.py`  

&nbsp;
## To Update the remote Repo with the new Package/Code
~/repoDir >>  
-    `cd v-env/lib/python3.8/site-packages`  
-    `aws lambda update-function-code --function-name my-function --zip-file fileb://function.zip`  
