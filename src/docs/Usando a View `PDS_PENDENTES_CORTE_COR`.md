# ✨ Teste SP ATUALIZA_IQC:

## **Recursos utilizados:**
### **View:** *`PDS_PENDENTES_CORTE_COR`*
### **Stored Procedure:** *`ATUALIZA_IQC`*

<br />

# 🔎 Estado antes de rodar a SP:
```SQL
SELECT
    REQUISICAO,
    CORTE,
    NR_ORDEM_CORTE,
    PD,
    MEDIDA,
    QTD_PD_REQ,
    QTD_CORTADA
FROM
    PDS_PENDENTES_CORTE_COR
WHERE
    CORTE IN (119156, 119150, 119145)
```

> | REQUISICAO | CORTE  | NR_ORDEM_CORTE | PD    | MEDIDA | QTD_PD_REQ | QTD_CORTADA |
> | :--------- | :----- | :------------- | :---- | :----- | :--------- | :---------- |
> | 126989     | 119156 | 20950          | 15881 | 930    | 100        | 0           |
> | 126989     | 119150 | 20949          | 15875 | 550    | 100        | 0           |
> | 126989     | 119145 | 20950          | 15870 | 450    | 100        | 0           |

# ⚡ Chamada 1:
```SQL
EXECUTE PROCEDURE ATUALIZA_IQC(126989, 119150, 100, 0.55)
```
<div style="color:#88f">

#### 👀 Resultado Esperado:
 > | REQUISICAO | CORTE  | NR_ORDEM_CORTE | PD    | MEDIDA | QTD_PD_REQ | QTD_CORTADA |
> | :--------- | :----- | :------------- | :---- | :----- | :--------- | :---------- |
> | 126989     | 119150 | 20949          | 15875 | 550    | 100        | 1           |


</div>
<div style="color: #8F8;" >

#### 😁 Resultado Obtido:

 > | REQUISICAO | CORTE  | NR_ORDEM_CORTE | PD    | MEDIDA | QTD_PD_REQ | QTD_CORTADA |
> | :--------- | :----- | :------------- | :---- | :----- | :--------- | :---------- |
> | 126989     | 119150 | 20949          | 15875 | 550    | 100        | 1           |


</div> 
<br />
<br />

# ⚡ Chamada 2: 
```SQL
EXECUTE PROCEDURE ATUALIZA_IQC(126989, 119145, 100, 0.45)
```

<div style="color: #88f;" >

#### 👀 Resultado Esperado:
> | REQUISICAO | CORTE  | NR_ORDEM_CORTE | PD    | MEDIDA | QTD_PD_REQ | QTD_CORTADA |
> | :--------- | :----- | :------------- | :---- | :----- | :--------- | :---------- |
> | 126989     | 119145 | 20950          | 15870 | 450    | 100        | 1           |

</div>

<div style="color: #8F8;" >

#### 😁 Resultado Obtido:

> | REQUISICAO | CORTE  | NR_ORDEM_CORTE | PD    | MEDIDA | QTD_PD_REQ | QTD_CORTADA |
> | :--------- | :----- | :------------- | :---- | :----- | :--------- | :---------- |
> | 126989     | 119145 | 20950          | 15870 | 450    | 100        | 1           |

</div> 


<br />
<br />

# ⚡ Chamada 3: 
```SQL
EXECUTE PROCEDURE ATUALIZA_IQC(126989, 119156, 100, 0.93)
```

<div style="color: #88f;" >

#### 👀 Resultado Esperado:
> | REQUISICAO | CORTE  | NR_ORDEM_CORTE | PD    | MEDIDA | QTD_PD_REQ | QTD_CORTADA |
> | :--------- | :----- | :------------- | :---- | :----- | :--------- | :---------- |
> | 126989     | 119156 | 20950          | 15881 | 930    | 100        | 1           |

</div>

<div style="color: #8F8;" >

#### 😁 Resultado Obtido:

> | REQUISICAO | CORTE  | NR_ORDEM_CORTE | PD    | MEDIDA | QTD_PD_REQ | QTD_CORTADA |
> | :--------- | :----- | :------------- | :---- | :----- | :--------- | :---------- |
> | 126989     | 119156 | 20950          | 15881 | 930    | 100        | 1           |

</div> 


<br />
<br />

# ⚡ Chamada 4: 
```SQL
EXECUTE PROCEDURE ATUALIZA_IQC(126989, 119156, 100, 92.07)
```

<div style="color: #88f;" >

#### 👀 Resultado Esperado:
> | REQUISICAO | CORTE  | NR_ORDEM_CORTE | PD    | MEDIDA | QTD_PD_REQ | QTD_CORTADA |
> | :--------- | :----- | :------------- | :---- | :----- | :--------- | :---------- |
> | 126989     | 119156 | 20950          | 15881 | 930    | 100        | 100         |

</div>

<div style="color: #8F8;" >

#### 😁 Resultado Obtido:
> | REQUISICAO | CORTE  | NR_ORDEM_CORTE | PD    | MEDIDA | QTD_PD_REQ | QTD_CORTADA |
> | :--------- | :----- | :------------- | :---- | :----- | :--------- | :---------- |
> | 126989     | 119156 | 20950          | 15881 | 930    | 100        | 100         |

</div> 


<br />
<br />


# 👀 Estado esperado após teste:

```SQL
SELECT
    REQUISICAO,
    CORTE,
    NR_ORDEM_CORTE,
    PD,
    MEDIDA,
    QTD_PD_REQ,
    QTD_CORTADA
FROM
    PDS_PENDENTES_CORTE_COR
WHERE
    CORTE IN (119156, 119150, 119145)
```

<div style="color:#88f">

> | Numero da Requisicao | CORTE  | NR ORDEM DECORTE | PD    | MEDIDA | QTD_TOTAL_REQUISICAO | QTD_CORTADA |
> | :------------------- | :----- | :--------------- | :---- | :----- | :------------------- | :---------- |
> | 126989               | 119156 | 20950            | 15881 | 930    | 100                  | 100         |
> | 126989               | 119150 | 20949            | 15875 | 550    | 100                  | 1           |
> | 126989               | 119145 | 20950            | 15870 | 450    | 100                  | 1           |

</div>
<div style="color:#8F8">

# 👏 Estado obtido após teste:

> | Numero da Requisicao | CORTE  | NR ORDEM DECORTE | PD    | MEDIDA | QTD_TOTAL_REQUISICAO | QTD_CORTADA |
> | :------------------- | :----- | :--------------- | :---- | :----- | :------------------- | :---------- |
> | 126989               | 119156 | 20950            | 15881 | 930    | 100                  | 100         |
> | 126989               | 119150 | 20949            | 15875 | 550    | 100                  | 1           |
> | 126989               | 119145 | 20950            | 15870 | 450    | 100                  | 1           |

</div>
