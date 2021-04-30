import yfinance as tf
import pandas as pd
import datetime

print('\nTimeframe em 5 minutos\n')
time_frame = '5'
time_frame = time_frame + 'm'
dias = input('Digite a quantidade de dias: ')
dias = dias + 'd'
porce = input('\nDigite a porcetagem: ')
porce = int(porce)
print('')


def converter_time(frame):
    frame.index = frame.index.tz_convert('America/Sao_Paulo')
    frame.index = frame.index.tz_localize(None)
    return frame


def data_nome():
    data_n = datetime.datetime.now().strftime('%Y-%m-%d')
    return data_n


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
    try:
        if call / total >= porcetagem:
            valor = (call / total)
            return ['Call', valor]
    except:
        return ['Call', 0]
    try:
        if put / total >= porcetagem:
            valor = (put / total)
            return ['Put', valor]
    except:
        return ['Put', 0]


def velas(frame):
    frame['Vela'] = 0
    frame.loc[ativo['Close'] > frame['Open'], 'Vela'] = 'Call'
    frame.loc[ativo['Close'] < frame['Open'], 'Vela'] = 'Put'
    frame.loc[ativo['Close'] == frame['Open'], 'Vela'] = 'Doji'


def ler(lista):
    par = open(lista, 'r')
    paridades = []
    for a in par:
        a = a.replace('\n', '')
        a = (a+'=X')
        paridades.append(a)
    return paridades


def medias(frame):
    frame['T_Media'] = abs(frame['Open'] - frame['Close'])


nome_data = data_nome()
ativos = ler('ativos.txt')
strhora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
strhora = str(strhora)
df_catalogar = pd.DataFrame(
    columns=['Hora', 'Paridade', 'Timeframe', 'Direção'], index=None)
for a in ativos:
    r_hora = 17
    r_minuto = 55
    ativo = tf.download(a, period=dias, interval=time_frame)
    ativo.drop(columns='Volume', inplace=True)
    converter_time(ativo)
    velas(ativo)
    medias(ativo)
    while r_hora > -1:
        r_hora -= 1
        if r_hora != -1:
            while r_minuto > -1:
                tempo = hora(r_hora, r_minuto, 0)
                df = listar(ativo, tempo)
                media = df['T_Media'].mean()
                cat = catalogacao(df, porce)
                if cat != None:
                    nome = a.split('=X')
                    nome = nome[0]
                    mlt = 0
                    if 'JPY' in nome:
                        mlt = 1000
                    else:
                        mlt = 100000

                    print(f'Ativo = {nome}')
                    print(f'Horario = {tempo.strftime("%H:%M:%S")}')
                    print(f'Porcetagem = {cat[1]*100:.2f}%')
                    print(f'Direção = {cat[0]}')
                    print(f'Media: {round(media*mlt)} Pontos')
                    print('')
                    df_catalogar = df_catalogar.append(
                        {'Hora': str(tempo.strftime("%H:%M:%S")), 'Paridade': nome, 'Timeframe': time_frame, 'Direção': cat[0]}, ignore_index=True)
                    open(nome_data + '_' + time_frame+'_.csv', 'a').write(
                        f'{str(tempo.strftime("%H:%M:%S"))};{nome};5M;{cat[0]}\n')
                r_minuto -= 5
            else:
                r_minuto = 55
print(f'Gerado arquivo com nome: {nome_data}_{time_frame}_.csv\n')
df_catalogar = df_catalogar.sort_values(by=['Hora'])
df_catalogar = df_catalogar.reset_index()
df_catalogar = df_catalogar.drop(['index'], 1)
try:
    df_catalogar.to_csv(nome_data + '_' + time_frame+'_.csv',
                        sep=';', header=False, index=False)
except:
    print(f'Sem sinal para gerar um arquivo de lista\n')

input(f'Pressione qualquer tecla para finalizar...')
