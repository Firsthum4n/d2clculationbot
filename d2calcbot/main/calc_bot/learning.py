from main.calc_bot.bot import encryption, DotaDataset, MainNetwork
from main.calc_bot.test_data import matches_test
import json
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from main.calc_bot.bot import encryption, DotaDataset, MainNetwork
from main.calc_bot.test_data import matches_test
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader


filepath = 'main/calc_bot/data.json'
data = []

# filepath_2 = 'main/calc_bot/data_winner.json'
x_data, y_data = matches_test()

# with open(filepath_2, 'w') as f:
#     json.dump(y_data, f, indent=4)

y_data = torch.tensor(y_data, dtype=torch.float32)


cnt = 66
x_valid_data = []
y_valid_data = []
for i in range(22):
    x_valid_data.append(x_data[cnt])
    y_valid_data.append(y_data[cnt])
    cnt+=1


x_data = x_data
y_data = y_data


radiant_team_data = DotaDataset(x_data, 'radiant', 0)
dire_team_data = DotaDataset(x_data, 'dire', 1)
r_valid = DotaDataset(x_valid_data, 'radiant', 0)
d_valid = DotaDataset(x_valid_data, 'dire', 1)




batch_size = 64

num_teams = 6
num_players = 10
num_heroes = 10
embedding_dim = 32

model = MainNetwork()

def custom_collate_fn(batch):
    radiant_d, dire_d = zip(*batch)

    return list(radiant_d), list(dire_d)

criterion = nn.BCELoss()
optimizer = torch.optim.AdamW(model.parameters(), lr=0.000001, weight_decay=1e-1)

EPOCHS = 350


for j in range(len(x_data)):
    r = radiant_team_data[j]
    d = dire_team_data[j]
    winner = y_data[j]
    winner = winner.unsqueeze(0)

    dataloader = DataLoader(list(zip(r, d)), batch_size=batch_size, collate_fn=custom_collate_fn)

    for epoch in range(EPOCHS):
        model.train()
        running_loss = 0.0


        for i, (radiant_batch, dire_batch) in enumerate(dataloader):
            optimizer.zero_grad()
            output = model(radiant_batch, dire_batch)
            output = output.squeeze(1)
            loss = criterion(output, winner)
            loss.backward(retain_graph=True)
            optimizer.step()
            running_loss += loss.item()

    if epoch + 1 == EPOCHS:
        data_item = {
            "number:": j + 1,
            "loss": running_loss / len(x_data),
            "out": output.item(),
            "winner": winner.item()

        }
        data.append(data_item)

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

        print(f'Epoch {epoch+1}, Loss: {running_loss / len(x_data):.4f}, out:{output.item()}, winner:{winner.item()}')
    print(f'данные номер: {j+1}')
print("Обучение завершено.")
torch.save(model.state_dict(), 'main/calc_bot/dota_model.pth')


model = MainNetwork()
model.load_state_dict(torch.load('main/calc_bot/dota_model.pth'))
for j in range(len(x_valid_data)):
    r = r_valid[j]
    d = d_valid[j]
    winner = y_valid_data[j]
    winner = winner.unsqueeze(0)
    valid_dataloader = DataLoader(list(zip(r, d)), batch_size=batch_size, shuffle=True)

    for epoch in range(EPOCHS):
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for i, (radiant_batch, dire_batch) in enumerate(valid_dataloader):
                output = model(radiant_batch, dire_batch)
                output = output.squeeze(1)
                loss = criterion(output,winner)
                val_loss += loss.item()

        print(f'Epoch {epoch + 1}, Val Loss: {val_loss / len(x_valid_data):.4f}')

print("Обучение завершено.")
torch.save(model.state_dict(), 'main/calc_bot/dota_model.pth')