
if @isdefined(base_path) && isfile("$base_path/Q_table")
    if !@isdefined(Q_table) || Q_TABLE == nothing
        const Q_TABLE = deserialize("$base_path/Q_table")
    end
else
    myid() == 1 && @warn "Q_table not found. Can't fit Optimal model"
end

get_qs(d::Datum) = valmap(Q_TABLE[hash(d)]) do q
    max.(q, NOT_ALLOWED)
end

struct Optimal{T} <: AbstractModel{T}
    cost::Float64
    β::T
    ε::T
end

default_space(::Type{M}) where M <: Optimal = Space(
    :cost => COSTS,
    :β => (1e-6, 50),
    # :β_expansion => # TODO
    :ε => (1e-3, 1)
)

features(::Type{M}, d::Datum) where M <: Optimal = (
    options = [0; get_frontier(d.t.m, d.b)],
    q = get_qs(d)
)

function action_dist!(p::Vector{T}, model::Optimal{T}, φ::NamedTuple) where T
    softmax_action_dist!(p, model, φ)
end

function preference(model::Optimal{T}, φ::NamedTuple, c::Int)::T where T
    model.β * φ.q[model.cost][c+1]
end

# For simulation

function get_qs(m::MetaMDP, b::Belief, cost::Float64)
    V = load_V(id(mutate(m, cost=cost)))
    Dict(cost => Q(V, b))
end

function action_dist(model::Optimal, m::MetaMDP, b::Belief)
    p = zeros(length(b) + 1)
    φ = (
        options = [0; get_frontier(m, b)],
        q = get_qs(m, b, model.cost)
    )
   action_dist!(p, model, φ)
end


# ---------- Souped up Optimal model ---------- #

struct OptimalPlus{T} <: AbstractModel{T}
    cost::Float64
    β_select::T
    β_term::T
    ε::T
end

default_space(::Type{OptimalPlus}) = Space(
    :cost => COSTS,
    :β_select => (1e-6, 50),
    :β_term => (1e-6, 50),
    :ε => (1e-3, 1)
)

function features(::Type{OptimalPlus{T}}, d::Datum) where T
    qs = get_qs(d)
    frontier = get_frontier(d.t.m, d.b)
    _optplus_features(T, qs, frontier)
end
_optplus_features(T, qs, frontier) = (
    frontier=frontier, 
    q_select=valmap(x->x[frontier.+1], qs),
    q_term=valmap(x->x[[1; frontier.+1]], qs),
    tmp_select=zeros(T, length(frontier)),
    tmp_term=zeros(T, length(frontier)+1),
)

function action_dist!(p::Vector{T}, model::OptimalPlus{T}, φ::NamedTuple) where T
    term_select_action_dist!(p, model, φ)
end

function selection_probability(model::OptimalPlus, φ::NamedTuple)
    q = φ.tmp_select
    q .= model.β_select .* φ.q_select[model.cost]
    softmax!(q)
end

function termination_probability(model::OptimalPlus, φ::NamedTuple)
    q = φ.tmp_term
    q .= model.β_term .* φ.q_term[model.cost]
    softmax!(q, 1)
end

# For simulation

function action_dist(model::OptimalPlus, m::MetaMDP, b::Belief)
    p = zeros(length(b) + 1)
    φ = _optplus_features(Float64, get_qs(m, b, model.cost), get_frontier(m, b))
   action_dist!(p, model, φ)
end

