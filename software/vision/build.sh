if (python setup.py build -f) then
    if (sudo python setup.py install -f) then
        python balltrackingscript.py
    fi
fi
