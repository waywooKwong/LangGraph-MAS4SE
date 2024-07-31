<template>
    <div class="joint-scope chatbot">
        <div ref="toolbar"></div>
        <div class="side-bar">
            <div class="toggle-bar">

                <div @click="goToChatView()" class="icon go-to-chat"
                     data-tooltip="返回对话界面"
                     data-tooltip-position-selector=".toggle-bar"></div>

                <div @click="toggleStencil()" class="icon toggle-stencil"
                     :class="{'disabled-icon': !stencilOpened}"
                     data-tooltip="Toggle Element Palette"
                     data-tooltip-position-selector=".toggle-bar"></div>
                <div @click="toggleJsonEditor()" class="icon toggle-editor"
                     :class="{'disabled-icon': !jsonEditorOpened}"
                     data-tooltip="Toggle JSON Editor"
                     data-tooltip-position-selector=".toggle-bar"></div>

                <div @click="sendJsonToServer()" class="icon commit-user-design"
                    :disabled="isUploading"
                     data-tooltip="提交设计结果"
                     data-tooltip-position-selector=".toggle-bar"></div>

                
                
            </div>
            <div v-show="stencilOpened" ref="stencil" class="stencil-container"></div>
        </div>
        <div class="main-container">
            <div ref="paper" class="paper-container"></div>
            <JsonEditor :content="fileJSON" v-show="jsonEditorOpened"/>
        </div>
        <Inspector/>
    </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Component from 'vue-class-component';
import { Subscription } from 'rxjs';
import { MessageBox } from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

import apiClient from '@/axios'; // Import apiClient

import JointPlusService from '../../services/joint-plus.service';
import JsonEditor from './Json-editor/Json-editor.vue';
import Inspector from './Inspector/Inspector.vue';
import { STENCIL_WIDTH } from '../../theme';
import { SharedEvents } from '../../joint-plus/controller';
import { importGraphFromJSON, loadStencilShapes, zoomToFit } from '../../joint-plus/actions';

import exampleGraphJSON from '../../joint-plus/config/example-graph.json';

@Component({
    components: {
        Inspector,
        JsonEditor
    }
})
export default class Chatbot extends Vue {

    public joint = null as JointPlusService;
    public stencilOpened = true;
    public jsonEditorOpened = true;
    public fileJSON = {};
    public isUploading = false; // 添加上传状态

    private subscriptions = new Subscription();

    public mounted(): void {
        const { $el, $refs: { paper, stencil, toolbar }, subscriptions, $eventBusService } = this;
        subscriptions.add(
            $eventBusService.subscribe(SharedEvents.GRAPH_CHANGED, (json: Object) => this.onJointGraphChange(json))
        );
        subscriptions.add(
            $eventBusService.subscribe(SharedEvents.JSON_EDITOR_CHANGED, (json: Object) => this.onJsonEditorChange(json))
        );

        this.joint = new JointPlusService(
            $el,
            paper as Element,
            stencil as Element,
            toolbar as Element,
            $eventBusService
        );
        this.setStencilContainerSize();
        this.onStart();
    }

    public beforeDestroy(): void {
        this.subscriptions.unsubscribe();
        this.joint.destroy();
    }

    public openFile(json: Object): void {
        const { joint } = this;
        this.fileJSON = json;
        importGraphFromJSON(joint, json);
        zoomToFit(joint);
    }

    public toggleJsonEditor(): void {
        this.jsonEditorOpened = !this.jsonEditorOpened;
    }

    public toggleStencil(): void {
        this.stencilOpened = !this.stencilOpened;
        this.onStencilToggle();
    }
    public goToChatView() {
        this.$router.push({ name: 'ChatView' }); // 路由跳转到 ChatView
    }
    // public async sendJsonToServer(): Promise<void> { //将json发送到服务器
    //     try {
    //         const response = await apiClient.post('/upload-agent', this.fileJSON);
    //         console.log('JSON sent successfully:', response.data);
    //     } catch (error) {
    //         console.error('Error sending JSON:', error);
    //     }
    // }
    public async sendJsonToServer(): Promise<void> {
        if (this.isUploading) return; // 如果正在上传则返回
        
        this.isUploading = true; // 开始上传时设置为 true

        try {
            // Convert JSON to a Blob
            const jsonBlob = new Blob([JSON.stringify(this.fileJSON)], { type: 'application/json' });
            // Create FormData and append the Blob
            const formData = new FormData();
            formData.append('file', jsonBlob, 'agent-jsonfile.json');

            // Send the FormData using axios with a timeout of 10 seconds
            const response = await apiClient.post('/upload-agent', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
                timeout: 10000 // 设置超时时间为10秒
            });
            this.openSuccess();
            console.log('JSON file sent successfully:', response.data);
        } catch (error) {
            if (error.code === 'ECONNABORTED') {
                this.openTimeout();
            } else {
                this.openFail();
            }
            console.error('Error sending JSON file:', error);
        }
        finally {
            this.isUploading = false; // 上传完成后设置为 false
        }
    }
   
    
    private openSuccess() {
        this.$message({
          message: '智能体结构上传成功',
          type: 'success'
        });
    }
    private openFail() {
        this.$message.error('智能体结构上传失败');
    }
    private openTimeout() {
        this.$message.error('智能体结构上传超时');
    }
    

    private onStart(): void {
        const { joint } = this;
        loadStencilShapes(joint);
        this.openFile(exampleGraphJSON);
    }

    private onJsonEditorChange(json: Object): void {
        const { joint } = this;
        if (joint) {
            importGraphFromJSON(joint, json);
        }
    }

    private onJointGraphChange(json: Object): void {
        this.fileJSON = json;
    }

    private setStencilContainerSize(): void {
        (this.$refs.stencil as HTMLDivElement).style.width = `${STENCIL_WIDTH}px`;
        this.onStencilToggle();
    }

    private onStencilToggle(): void {
        const { joint, stencilOpened } = this;
        const { scroller, stencil } = joint;
        if (stencilOpened) {
            stencil.unfreeze();
            scroller.el.scrollLeft += STENCIL_WIDTH;
        } else {
            stencil.freeze();
            scroller.el.scrollLeft -= STENCIL_WIDTH;
        }
    }
}
</script>

<style lang="scss">
@import "src/assets/fonts";

.chatbot {
    position: relative;
    width: 100%;
    height: 100%;
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: realist, sans-serif;
    display: flex;
    min-width: 900px;

    .main-container {
        display: flex;
        flex-flow: column;
        height: 100%;
        overflow: hidden;
        flex: 1;

        /*  Diagram  */
        .paper-container {
            position: relative;
            overflow: hidden;
            box-sizing: border-box;
            z-index: 1;
            flex: 1;
            background: #F8F9FA;
        }
    }

    /*  Sidebar  */
    .side-bar {
        height: 100%;
        max-width: 250px;
        z-index: 2;
        background: none;
        display: flex;

        .toggle-bar {
            height: 100%;
            width: 50px;
            background: #222222;
            z-index: 2;
            display: flex;
            flex-flow: column;
            align-items: center;
            padding: 13px;

            .icon {
                margin-bottom: 26px;
                font-size: 24px;
                color: #FFFFFF;
                cursor: pointer;

                &:before {
                    @include icon;
                }
                &.disabled-icon {
                    opacity: 0.35;
                    cursor: not-allowed; /* 添加禁止图标 */
                }

                &[disabled] {
                    cursor: not-allowed; /* 添加禁止图标 */
                }
            }

            .toggle-stencil {
                &:before {
                    content: '\E39D'
                }
            }

            .toggle-editor {
                &:before {
                    content: '\E86F'
                }
            }

            .go-to-chat {
                &:before {
                    content: '\E8AF'
                }
            }

            .commit-user-design {
                &:before {
                    content: '\E92F'
                }
            }
            
            


            .disabled-icon {
                opacity: 0.35;
            }
        }

        .stencil-container {
            height: 100%;
            position: relative;
        }
    }
}
</style>
