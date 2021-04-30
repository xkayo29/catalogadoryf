import yfinance as tf
import pandas as pd
import datetime


def converter_time(index):
    index.index = index.index.tz_convert('America/Sao_Paulo')
    index.index = index.index.tz_localize(None)
    return index


def hora(hora, minuto, segundo):
    tempo = datetime.time(hora, minuto, segundo)
    return tempo


def listar(frame, tempo):
    novo_frame = frame.loc[tempo]
    return novo_frame


def catalogacao(frame, porcetagem):
    call, put, doji = 0, 0, 0
    porcetagem = porcetagem / 100
    for _, v in frame.iterrows():
        if v['Vela'] == 'Call':
            call += 1
        elif v['Vela'] == 'Put':
            put += 1
        else:
            doji += 1
    total = call + put + doji

    if call / total > porcetagem:
        valor = (call / total)
        return ['Call', valor]

    elif put / total > porcetagem:
        valor = (put / total)
        return ['Put', valor]

    else:
        return None


def velas(frame):
    frame['Vela'] = 0
    frame.loc[ativo['Close'] > frame['Open'], 'Vela'] = 'Call'
    frame.loc[ativo['Close'] < frame['Open'], 'Vela'] = 'Put'
    frame.loc[ativo['Close'] == frame['Open'], 'Vela'] = 'Doji'


print(f'\nFormato da lista = 03:35:00;EURUSD;5M;Call')
print(f'Arquivo com final = ".csv"\n')
arq = input('Digite o nome do arquivo (Ex: lista.csv): ')
csv = pd.read_csv(arq, header=None, sep=';')
cont_w = 0
cont_l = 0
rate = 0
cont_s = 1
df_listar = pd.DataFrame(
    columns=['Hora', 'Paridade', 'Timeframe', 'Direção', 'Resultado'], index=None)
for _, l in csv.iterrows():
    erro = False
    a = f'{l[1]}=X'
    ativo = tf.download(a, period='1d', interval=l[2])
    converter_time(ativo)
    velas(ativo)

    try:
        direc = ativo.loc[l[0]]['Vela']

    except:
        print(f'{cont_s} - {l[1]} *|{l[0]}|* horario nao encontrado')
        cont_s += 1
        erro = True
    if not erro:

        try:
            if direc == l[3]:
                print(
                    f'{cont_s} - {l[1]} | Horario: {l[0]} | Direção: {l[3]} - "WIN"\n')
                df_listar = df_listar.append(
                    {'Hora': l[0], 'Paridade': l[1], 'Timeframe': l[2], 'Direção': l[3], 'Resultado': 'WIN'}, ignore_index=True)
                cont_w += 1
                cont_s += 1
            else:
                print(
                    f'{cont_s} - {l[1]} | Horario: {l[0]} | Direção: {l[3]} - "LOSS"\n')
                df_listar = df_listar.append(
                    {'Hora': l[0], 'Paridade': l[1], 'Timeframe': l[2], 'Direção': l[3], 'Resultado': 'LOSS'}, ignore_index=True)
                cont_l += 1
                cont_s += 1
        except NameError:
            print(f'{l[1]} ainda nao houve sinal')
    else:
        print('')
print(f'Total WIN = {cont_w}')
print(f'Total LOSS = {cont_l}')
print(f'Total = {cont_w + cont_l}')
df_listar.to_csv('check.csv', index=False)
input(f'Pressione qualquer tecla para finalizar...')
