import disnake
from disnake.ext import commands
import random
from utils import database


class Economic(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.db = database.DataBase()

	@commands.command(
		name="баланс",
		aliases=["cash", "balance"],
		brief="Вывод баланса пользователя",
		usage="balance <@user>"
	)
	async def user_balance(self, ctx, member: disnake.Member=None):
		balance = await self.db.get_data(ctx.author)
		embed = disnake.Embed(
			description=f"Баланса пользователя __{ctx.author}__: **{balance['balance']}**"
		)

		if member is not None:
			balance = await self.db.get_data(member)
			embed.description = f"Баланса пользователя __{member}__: **{balance['balance']}**"
		await ctx.send(embed=embed)
	@commands.command(
		name='заработать',
		aliases=['working'],
		brief='ну заработать бобла',
		usage='work'
		)
	async def work(self, ctx):
		balance = await self.db.get_data(ctx.author)
		a = random.randint(0, 500)
		

		embed = disnake.Embed(
			description=f'Вы заработали ' + a 
		)
		await self.db.update_member(ctx.author, {'$inc': {'balance': a}})
	@commands.command(
		name='украсть',
		aliases=['crimebank'],
		brief='украсть деньги с банка',
		usage='crime')
	async def crime(self, ctx):
		balance = await self.db.get_data(ctx.author)
		embed = disnake.Embed()
		a = random.randint(0,2)
		b = random.randint(0,1000)
		if a == 1:
			embed.description('Вас заметил охраник и дал штрах ' + b)
			await self.db.update_member(ctx.author, {"$inc": {"balance": -b}})
		elif a == 2:
			embed.description('Вы украли деньги! ' + b)
			await self.db.update_member(ctx.author, {"$inc": {"balance": b}})
	@commands.command(
		name="перевод",
		aliases=["give-cash", "givecash", "pay"],
		brief="Перевод денег другому пользователю",
		usage="pay <@user> <amount>"
	)
	async def pay_cash(self, ctx, member: disnake.Member, amount: int):
		balance = await self.db.get_data(ctx.author)
		embed = disnake.Embed()

		if member.id == ctx.author.id:
			embed.description = f"__{ctx.author}__, конечно извините меня, но проход жучкам сегодня закрыт."

		if amount <= 0:
			embed.description = f"__{ctx.author}__, конечно извините меня, но проход жучкам сегодня закрыт."
		elif balance["balance"] <= 0:
			embed.description = f"__{ctx.author}__, недостаточно средств"
		else:
			await self.db.update_member(ctx.author, {"$inc": {"balance": -amount}})
			await self.db.update_member(member, {"$inc": {"balance": amount}})

			embed.description = f"__{ctx.author}__, транзакция прошла успешно"

		await ctx.send(embed=embed, delete_after=5)


def setup(bot):
	bot.add_cog(Economic(bot))
