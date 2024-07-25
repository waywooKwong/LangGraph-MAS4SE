<template>
  <div class="agent-map">
    <div class="sidebar">
      <button @click="addAgentNode">添加智能体</button>
    </div>
    <div id="paper"></div>
  </div>
</template>

<script>
import { dia, shapes } from '@joint/core';
import { createApp, h } from 'vue';
import AgentNode from '@/components/AgentNode.vue';

export default {
  name: 'AgentMap',
  data() {
    return {
      graph: null,
      paper: null,
      agentCounter: 0,
    };
  },
  mounted() {
    this.graph = new dia.Graph();

    this.paper = new dia.Paper({
      el: document.getElementById('paper'),
      model: this.graph,
      width: 1000,
      height: 800,
      gridSize: 10,
      drawGrid: true,
    });

    this.paper.on('element:pointerdblclick', (elementView) => {
      this.graph.getCell(elementView.model).remove();
    });
  },
  methods: {
    addAgentNode() {
      const agentNode = new shapes.standard.Rectangle();
      agentNode.position(100, 100);
      agentNode.resize(200, 100);
      agentNode.attr({
        body: {
          fill: 'white',
          stroke: 'black',
        },
      });

      this.graph.addCell(agentNode);

      const foreignObject = new dia.Element({
        position: { x: 100, y: 100 },
        size: { width: 200, height: 100 },
        attrs: {
          fo: {
            tagName: 'foreignObject',
            width: '100%',
            height: '100%',
            x: 0,
            y: 0,
            stroke: 'none',
            fill: 'none',
            html: `
              <div xmlns="http://www.w3.org/1999/xhtml" style="width:100%;height:100%;">
                <div id="vue-container-${agentNode.id}" class="agent-node-container"></div>
              </div>
            `,
          },
        },
      });

      this.graph.addCell(foreignObject);

      const html = document.getElementById(`vue-container-${agentNode.id}`);

      createApp({
        render: () =>
          h(AgentNode, {
            nodeId: agentNode.id,
            graph: this.graph,
          }),
      }).mount(html);
    },
  },
};
</script>

<style scoped>
.agent-map {
  display: flex;
}

.sidebar {
  width: 200px;
  padding: 10px;
  background: #f1f1f1;
  border-left: 1px solid #ddd;
}

#paper {
  flex: 1;
  position: relative;
}

.agent-node-container {
  width: 100%;
  height: 100%;
}
</style>
