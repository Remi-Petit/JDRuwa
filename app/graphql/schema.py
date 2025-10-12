import strawberry
from strawberry.fastapi import GraphQLRouter
from app.graphql.resolvers.user_resolvers import Query as UserQuery, Mutation as UserMutation
from app.graphql.resolvers.auth_resolvers import AuthMutations
from app.graphql.resolvers.protected_resolvers import ProtectedQueries
from app.graphql.context import get_context

@strawberry.type
class Query(UserQuery, ProtectedQueries):
    pass

@strawberry.type
class Mutation(UserMutation, AuthMutations):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema, context_getter=get_context)
