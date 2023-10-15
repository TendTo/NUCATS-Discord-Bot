from discord.ext import commands

from config import Config
import tools


class CommitteePoints(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_role(Config.get("COMMITTEE_ROLE"))
    @commands.guild_only()
    async def points(self, ctx, name):
        if ctx.channel.id not in Config.get("COMMITTEE_GROUP"):
            return

        name = name.lower()
        if name in ["all", "*"]:
            results = await tools.query_select(f"""SELECT * FROM committee_points;""")
            await ctx.channel.send("**Committee Points:**")
            for item in results:
                await ctx.channel.send(f"{item[0]} - {item[1]}".capitalize())
        else:
            results = await tools.query_select(f"""SELECT * FROM committee_points WHERE id = "{name}";""")
            await ctx.channel.send(f"{results[0][0]} has {results[0][1]} points".capitalize())

    @commands.command()
    @commands.has_role(Config.get("COMMITTEE_ROLE"))
    @commands.guild_only()
    async def add_points(self, ctx, name, value):
        if ctx.channel.id not in Config.get("COMMITTEE_GROUP"):
            return

        name = name.lower()
        points = await tools.query_select(f"""SELECT * FROM committee_points WHERE id = "{name}";""")
        points2 = points[0][1] + int(value)
        if await tools.query_insert(f"""UPDATE committee_points SET points = {points2} WHERE id = "{name}";"""):
            await ctx.channel.send(f"Added {value} points to {name.capitalize}!")
        else:
            await ctx.channel.send(f"Error - Failed to update the database")

    @commands.command()
    @commands.has_role(Config.get("COMMITTEE_ROLE"))
    @commands.guild_only()
    async def add_user(self, ctx, name):
        if ctx.channel.id not in Config.get("COMMITTEE_GROUP"):
            return

        name = name.lower()
        if await tools.query_insert(f"""INSERT INTO committee_points(id,points) VALUES("{name}", 0)"""):
            await ctx.channel.send(f"Added {name.capitalize()}")
        else:
            await ctx.channel.send(f"Error - Failed to update database")


async def setup(client):
    await client.add_cog(CommitteePoints(client))
