from environment import Environment
from agents.bayesian_agent import BayesianAgentRule1, BayesianAgentRule2
from agents.min_action_agent import MinActionAgent

env = Environment(10, place_target_in="cave")
print(f"Target: {env.target}, terrain: {env.get_terrain(*env.target)}")
# env.show()


agent = BayesianAgentRule1(env)
agent.run()
print(f"{agent.__class__}: Search Count - {agent.search_count}, Total Actions - {agent.total_actions()}")
#
agent = BayesianAgentRule2(env)
agent.run()
print(f"{agent.__class__}: Search Count - {agent.search_count}, Total Actions - {agent.total_actions()}")
#
agent = MinActionAgent(env)
agent.run()
print(f"{agent.__class__}: Search Count - {agent.search_count}, Total Actions - {agent.total_actions()}")