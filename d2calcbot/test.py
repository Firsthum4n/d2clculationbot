import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader


from main.calc_bot.bot import encryption, DotaDataset, MainNetwork
from main.calc_bot.test_data import matches_test


x_data, y_data = matches_test()
y_data = torch.tensor(y_data, dtype=torch.float32)


radiant_team_data = DotaDataset(x_data, 'radiant', 0)
dire_team_data = DotaDataset(x_data, 'dire', 1)



r = radiant_team_data[0]
d = dire_team_data[0]
print(len(r))


winner = y_data[0]

batch_size = 64
dataloader = DataLoader(list(zip(radiant_team_data, dire_team_data)), batch_size=batch_size, shuffle=True)

num_teams = 6
num_players = 10
num_heroes = 10
embedding_dim = 32

model = MainNetwork(num_teams, num_players, num_heroes, embedding_dim)
output = model(r, d)

criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

EPOCHS = 5


for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0
    for i, (radiant_batch, dire_batch) in enumerate(dataloader):
        optimizer.zero_grad()
        output = model(radiant_batch[0], dire_batch[0]) #Передаем данные в модель
        output = output.squeeze(1) # Убираем лишнее измерение
        loss = criterion(output, y_data[i])
        loss.backward()
        optimizer.step()
        running_loss += loss.item()

    print(f'Epoch {epoch+1}, Loss: {running_loss / len(x_data):.4f}')

print("Обучение завершено.")
