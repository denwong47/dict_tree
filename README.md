# dict_tree
 A simple class to manage temporary Environment Variables as a context manager.

 ## dict_tree.DictionaryTree()
 ## Syntax:
 ```
 dict_tree.DictionaryTree(
     obj,
     name:str="",
     box:dict_tree.boxes.Box=dict_tree.boxes.ThinBox,
     indent:int=6,
     echo:bool=True,
 )

 ```
 `obj` can be any object. It is however not meaningful to call the function with and object that does not have a `__dict__` property.

 `name` is the title of the tree at the root node; if unspecified, the type and id() of the object will be displayed.

 `box` defines the set of UTF-8 characters to draw the boxes with.
 There are 3 options:
 - `dict_tree.boxes.ThinBox` (default)
 - `dict_tree.boxes.ThickBox`
 - `dict_tree.boxes.DoubleBox`
 See below for examples.

 `indent` is how far subbranches should project beyond the parent branch.

 If `echo` is `True`, the tree is immediately printed to `stdout`. Otherwise, you can call `str()` on an instance of `DictionaryTree` which will return the tree in `str`.


 Sample obj:
 ```
    [
        {
            "name": "power_singlefield_with_unit",
            "type": "STRING",
            "mode": "NULLABLE"
        },
        {
            "name": "s_farbe_kombifeld",
            "type": "STRING",
            "mode": "NULLABLE"
        },
        {
            "name": "t_productfeature",
            "type": "RECORD",
            "mode": "REPEATED",
            "fields": [
                {
                    "name": "ID",
                    "type": "STRING",
                    "mode": "NULLABLE"
                },
                {
                    "name": "Kurztext",
                    "type": "STRING",
                    "mode": "NULLABLE"
                },
                {
                    "name": "Text",
                    "type": "STRING",
                    "mode": "NULLABLE",
                    "fields": [
                        {
                            "name": "ID",
                            "type": "STRING",
                            "mode": "NULLABLE"
                        },
                        {
                            "name": "Kurztext",
                            "type": "STRING",
                            "mode": "NULLABLE"
                        },
                        {
                            "name": "Text",
                            "type": "STRING",
                            "mode": "NULLABLE"
                        }
                    ]
                }
            ]
        },
        {
            "name": "s_montageart",
            "type": "STRING",
            "mode": "NULLABLE"
        },

    ]
 ```

 Output wth `box`=`dict_tree.boxes.ThinBox`:
 ```
╾─────┬ Instance of [list] at address [0x7fc4b1602a40]    list    
      ├─────┬ [0]                                         dict    
      │     ├────── name                                  str     power_singlefield_with_unit
      │     ├────── type                                  str     STRING
      │     └────── mode                                  str     NULLABLE
      ├─────┬ [1]                                         dict    
      │     ├────── name                                  str     s_farbe_kombifeld
      │     ├────── type                                  str     STRING
      │     └────── mode                                  str     NULLABLE
      ├─────┬ [2]                                         dict    
      │     ├────── name                                  str     t_productfeature
      │     ├────── type                                  str     RECORD
      │     ├────── mode                                  str     REPEATED
      │     └─────┬ fields                                list    
      │           ├─────┬ [0]                             dict    
      │           │     ├────── name                      str     ID
      │           │     ├────── type                      str     STRING
      │           │     └────── mode                      str     NULLABLE
      │           ├─────┬ [1]                             dict    
      │           │     ├────── name                      str     Kurztext
      │           │     ├────── type                      str     STRING
      │           │     └────── mode                      str     NULLABLE
      │           └─────┬ [2]                             dict    
      │                 ├────── name                      str     Text
      │                 ├────── type                      str     STRING
      │                 ├────── mode                      str     NULLABLE
      │                 └─────┬ fields                    list    
      │                       ├─────┬ [0]                 dict    
      │                       │     ├────── name          str     ID
      │                       │     ├────── type          str     STRING
      │                       │     └────── mode          str     NULLABLE
      │                       ├─────┬ [1]                 dict    
      │                       │     ├────── name          str     Kurztext
      │                       │     ├────── type          str     STRING
      │                       │     └────── mode          str     NULLABLE
      │                       └─────┬ [2]                 dict    
      │                             ├────── name          str     Text
      │                             ├────── type          str     STRING
      │                             └────── mode          str     NULLABLE
      └─────┬ [3]                                         dict    
            ├────── name                                  str     s_montageart
            ├────── type                                  str     STRING
            └────── mode                                  str     NULLABLE
 ```
 Output wth `box`=`dict_tree.boxes.ThickBox`:
 ```
━━━━━━┳ Instance of [list] at address [0x7f4758606a80]    list    
      ┣━━━━━┳ [0]                                         dict    
      ┃     ┣━━━━━━ name                                  str     power_singlefield_with_unit
      ┃     ┣━━━━━━ type                                  str     STRING
      ┃     ┗━━━━━━ mode                                  str     NULLABLE
      ┣━━━━━┳ [1]                                         dict    
      ┃     ┣━━━━━━ name                                  str     s_farbe_kombifeld
      ┃     ┣━━━━━━ type                                  str     STRING
      ┃     ┗━━━━━━ mode                                  str     NULLABLE
      ┣━━━━━┳ [2]                                         dict    
      ┃     ┣━━━━━━ name                                  str     t_productfeature
      ┃     ┣━━━━━━ type                                  str     RECORD
      ┃     ┣━━━━━━ mode                                  str     REPEATED
      ┃     ┗━━━━━┳ fields                                list    
      ┃           ┣━━━━━┳ [0]                             dict    
      ┃           ┃     ┣━━━━━━ name                      str     ID
      ┃           ┃     ┣━━━━━━ type                      str     STRING
      ┃           ┃     ┗━━━━━━ mode                      str     NULLABLE
      ┃           ┣━━━━━┳ [1]                             dict    
      ┃           ┃     ┣━━━━━━ name                      str     Kurztext
      ┃           ┃     ┣━━━━━━ type                      str     STRING
      ┃           ┃     ┗━━━━━━ mode                      str     NULLABLE
      ┃           ┗━━━━━┳ [2]                             dict    
      ┃                 ┣━━━━━━ name                      str     Text
      ┃                 ┣━━━━━━ type                      str     STRING
      ┃                 ┣━━━━━━ mode                      str     NULLABLE
      ┃                 ┗━━━━━┳ fields                    list    
      ┃                       ┣━━━━━┳ [0]                 dict    
      ┃                       ┃     ┣━━━━━━ name          str     ID
      ┃                       ┃     ┣━━━━━━ type          str     STRING
      ┃                       ┃     ┗━━━━━━ mode          str     NULLABLE
      ┃                       ┣━━━━━┳ [1]                 dict    
      ┃                       ┃     ┣━━━━━━ name          str     Kurztext
      ┃                       ┃     ┣━━━━━━ type          str     STRING
      ┃                       ┃     ┗━━━━━━ mode          str     NULLABLE
      ┃                       ┗━━━━━┳ [2]                 dict    
      ┃                             ┣━━━━━━ name          str     Text
      ┃                             ┣━━━━━━ type          str     STRING
      ┃                             ┗━━━━━━ mode          str     NULLABLE
      ┗━━━━━┳ [3]                                         dict    
            ┣━━━━━━ name                                  str     s_montageart
            ┣━━━━━━ type                                  str     STRING
            ┗━━━━━━ mode                                  str     NULLABLE
 ```
 Output wth `box`=`dict_tree.boxes.DoubleBox`:
 ```
══════╦ Instance of [list] at address [0x7ff9d0ad6b40]    list    
      ╠═════╦ [0]                                         dict    
      ║     ╠══════ name                                  str     power_singlefield_with_unit
      ║     ╠══════ type                                  str     STRING
      ║     ╚══════ mode                                  str     NULLABLE
      ╠═════╦ [1]                                         dict    
      ║     ╠══════ name                                  str     s_farbe_kombifeld
      ║     ╠══════ type                                  str     STRING
      ║     ╚══════ mode                                  str     NULLABLE
      ╠═════╦ [2]                                         dict    
      ║     ╠══════ name                                  str     t_productfeature
      ║     ╠══════ type                                  str     RECORD
      ║     ╠══════ mode                                  str     REPEATED
      ║     ╚═════╦ fields                                list    
      ║           ╠═════╦ [0]                             dict    
      ║           ║     ╠══════ name                      str     ID
      ║           ║     ╠══════ type                      str     STRING
      ║           ║     ╚══════ mode                      str     NULLABLE
      ║           ╠═════╦ [1]                             dict    
      ║           ║     ╠══════ name                      str     Kurztext
      ║           ║     ╠══════ type                      str     STRING
      ║           ║     ╚══════ mode                      str     NULLABLE
      ║           ╚═════╦ [2]                             dict    
      ║                 ╠══════ name                      str     Text
      ║                 ╠══════ type                      str     STRING
      ║                 ╠══════ mode                      str     NULLABLE
      ║                 ╚═════╦ fields                    list    
      ║                       ╠═════╦ [0]                 dict    
      ║                       ║     ╠══════ name          str     ID
      ║                       ║     ╠══════ type          str     STRING
      ║                       ║     ╚══════ mode          str     NULLABLE
      ║                       ╠═════╦ [1]                 dict    
      ║                       ║     ╠══════ name          str     Kurztext
      ║                       ║     ╠══════ type          str     STRING
      ║                       ║     ╚══════ mode          str     NULLABLE
      ║                       ╚═════╦ [2]                 dict    
      ║                             ╠══════ name          str     Text
      ║                             ╠══════ type          str     STRING
      ║                             ╚══════ mode          str     NULLABLE
      ╚═════╦ [3]                                         dict    
            ╠══════ name                                  str     s_montageart
            ╠══════ type                                  str     STRING
            ╚══════ mode                                  str     NULLABLE
 ```
 