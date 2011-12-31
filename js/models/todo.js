define(['underscore', 'backbone'], function(_, Backbone) {
  var TodoModel = Backbone.Model.extend({
    url: "/todos",
    // Default attributes for the todo.
    defaults: {
      content: "empty todo...",
      done: false,
      order: 0
    },

    // Ensure that each todo created has `content`.
    initialize: function() {
      if (!this.get("content")) {
        this.set({"content": this.defaults.content});
      }
    }
  });
  return TodoModel;
});
